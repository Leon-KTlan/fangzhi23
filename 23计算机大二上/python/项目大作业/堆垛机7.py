import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.font_manager as fm
import random
from collections import deque
from numba import jit
import time

# Set up a font that supports Chinese characters
plt.rcParams['font.sans-serif'] = ['SimHei']  # Use SimHei font for Chinese characters
plt.rcParams['axes.unicode_minus'] = False  # Ensure minus sign is displayed correctly

# 全局变量，用于记录是否需要暂停以及暂停的时间
pause_until = None
global_target_position = None
global_io=0
stats = "节拍数:0\n已完成:\n状态: 装卸货中"


class ASRSSimulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.storage = np.zeros((2, width, height), dtype=np.int16)
        self.crane_pos = [0, 0, 0]  # [side, x, y]
        self.beat = 0
        self.operations = deque()
        self.total_operations = 0
        self.completed_operations = 0 
        self.current_path = []
        self.is_loading = False
        self.current_operation = None
        
        self.p1_pos = [self.width // 5, 2 * self.height // 3]
        self.p2_pos = [2 * self.width // 3, self.height // 5]

    def add_operation(self, io, item_no):
        self.operations.append((io, item_no))
        self.total_operations += 1

    @staticmethod
    @jit(nopython=True)
    def find_locations(storage, target):
        return np.argwhere(storage == target)

    def find_empty_location(self):
        empty_locations = self.find_locations(self.storage, 0)
        return tuple(empty_locations[np.random.randint(len(empty_locations))]) if len(empty_locations) > 0 else None

    def find_item_location(self, item_no):
        locations = self.find_locations(self.storage, item_no)
        return tuple(locations[0]) if len(locations) > 0 else None

    def calculate_path(self, start, end):
        path = []
        current = list(start)
        target = list(end)
        
        while current != target:
            if current[0] != target[0]:
                current[0] = target[0]
            elif current[1] != target[1]:
                current[1] += 1 if target[1] > current[1] else -1
            elif current[2] != target[2]:
                current[2] += 1 if target[2] > current[2] else -1
            path.append(list(current))
        
        return path

    def step(self):
        global global_target_position  # 声明全局变量
        global global_io
        if not self.current_path and not self.is_loading:
            if self.current_operation is not None:
                if self.crane_pos == [0, 0, 0]or self.crane_pos == [1, 0, 0]:
                    with open('log.txt', 'a') as file:#数据存表
                        if global_target_position is not None and global_io!=0:
                            d,x,y=global_target_position
                            file.write(f'io:{global_io} d:{d} x:{x} y:{y} Beat:{self.beat}\n')
                            global_target_position= None
                            global_io=0
                    self.completed_operations += 1
                    self.current_operation = None
                    if self.operations:
                        self.beat+=1
                        io, item_no = self.operations.popleft()
                        target = self.find_item_location(item_no)
                        global_target_position = target
                        global_io=io
                        if target is None:
                            return False
                        self.current_operation = (io, item_no)
                        if io == 1:
                            print("store",target)
                            self.current_path = self.calculate_path(self.crane_pos, target)
                        else:
                            print("re",target)
                            self.current_path = self.calculate_path(self.crane_pos, target)
                        self.is_loading = True
                    else:
                        return True
                else:
                    d,x,y=global_target_position
                    if d==0:
                        self.current_path = self.calculate_path(self.crane_pos, [0, 0, 0])
                    elif d==1:
                        self.current_path = self.calculate_path(self.crane_pos, [1, 0, 0])
            else:
                if self.operations:
                    io, item_no = self.operations.popleft()
                    target = self.find_item_location(item_no)
                    global_target_position = target
                    global_io=io
                    if target is None:
                        return False
                    self.current_operation = (io, item_no)
                    if io == 1:
                        print("store",target)
                        self.current_path = self.calculate_path(self.crane_pos, target)
                    else:
                        print("re",target)
                        self.current_path = self.calculate_path(self.crane_pos, target)
                    self.is_loading = True

        if self.current_path:
            self.crane_pos = self.current_path.pop(0)
            self.beat += 1
            if not self.current_path:
                self.is_loading = False
                if global_target_position is not None and tuple(self.crane_pos) == global_target_position:
                    #pause_until = time.time() + 1  # 设置暂停1秒
                    self.beat += 1 

        return True

    def get_state(self):
        return {
            'storage': self.storage,
            'crane_pos': self.crane_pos,
            'beat': self.beat,
            'operations_left': len(self.operations),
            'completed_operations': self.completed_operations,
            'total_operations': self.total_operations,
            'is_loading': self.is_loading
        }




def visualize_asrs(asrs):
    global pause_until
    global stats
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    plt.subplots_adjust(bottom=0.2)
    fig.suptitle('AS/RS 模拟系统')

    ax1.set_title('左侧存储区')
    ax2.set_title('右侧存储区')
    
    for ax in [ax1, ax2]:
        ax.set_xlim(0, asrs.width)
        ax.set_ylim(asrs.height, 0)
        ax.grid(True)
        ax.set_xlabel('X 坐标')
        ax.set_ylabel('Y 坐标')

    storage_left = ax1.imshow(np.zeros((asrs.height, asrs.width)), 
                            cmap='Blues', vmin=0, vmax=1)
    storage_right = ax2.imshow(np.zeros((asrs.height, asrs.width)), 
                             cmap='Reds', vmin=0, vmax=1)

    crane_left, = ax1.plot([], [], 'go', markersize=10, label='堆垛机')
    crane_right, = ax2.plot([], [], 'go', markersize=10, label='堆垛机')

   # ax1.plot(asrs.p1_pos[0], asrs.p1_pos[1], 'r*', markersize=10, label='P1')
   # ax2.plot(asrs.p2_pos[0], asrs.p2_pos[1], 'r*', markersize=10, label='P2')

    stats_text = ax1.text(0.02, -0.8, '', transform=ax1.transAxes)
    
    def update(frame):
        global pause_until
        global stats  # 声明全局变量 stats
        state = asrs.get_state()

        # 如果当前需要暂停，检查是否已经过了暂停时间
        if pause_until is not None and time.time() < pause_until:
            return [storage_left, storage_right, crane_left, crane_right, stats_text]

        if not asrs.step():
            return []

        # 更新存储区视图
        storage_left.set_array(state['storage'][0])
        storage_right.set_array(state['storage'][1])

        # 更新堆垛机位置
        if state['crane_pos'][0] == 0:
            crane_left.set_data([state['crane_pos'][1]], [state['crane_pos'][2]])
            crane_right.set_data([], [])
        else:
            crane_left.set_data([], [])
            crane_right.set_data([state['crane_pos'][1]], [state['crane_pos'][2]])


        # 更新状态信息

        d,x,y=state['crane_pos']
        if state['crane_pos'] == [0, 0, 0] or state['crane_pos'] == [1, 0, 0] or (global_target_position is not None and tuple(state['crane_pos']) == global_target_position):
                #ax1.plot(x,y, 'g.', markersize=10)标记坐标点
                pause_until = time.time() + 1  # 设置暂停1秒
                stats = "节拍数: {}\n已完成: {}/{}\n状态: 装卸货中".format(state['beat'], state['completed_operations'], state['total_operations'])
        else:
            if state['is_loading'] and global_io == 1:
                stats = "节拍数: {}\n已完成: {}/{}\n状态: 入库中".format(state['beat'], state['completed_operations'], state['total_operations'])
            elif state['is_loading'] and global_io == -1:
                stats = "节拍数: {}\n已完成: {}/{}\n状态: 出库中".format(state['beat'], state['completed_operations'], state['total_operations'])
            else:
                stats = "节拍数: {}\n已完成: {}/{}\n状态: 返回中".format(state['beat'], state['completed_operations'], state['total_operations'])

        stats_text.set_text(stats)

        return [storage_left, storage_right, crane_left, crane_right, stats_text]

    ani = FuncAnimation(fig, update, frames=None, 
                       interval=100, repeat=False, save_count=1000)
    plt.show()


def main():
    width, height = 200, 80
    asrs = ASRSSimulation(width, height)
    num=1
    tnum=1
    while True:
        user_input = input("输入 'exit' 以结束循环: ")
        if user_input == 'exit':
            break
        t=random.random()*2.4
        if(t>1):
            io=1
        else:
            io=-1
        item_no=None
        if io==1:
            item_no =num
            target=asrs.find_empty_location()
            if target==None:
                continue
            num+=1
            d, x, y = target
            asrs.storage[d, x, y] = item_no
        elif io==-1 and num>tnum:
            item_no=tnum
            print(item_no)
            if asrs.find_item_location(item_no)==None:
                continue
            tnum+=1
        if item_no is not None:
            asrs.add_operation(io, item_no)
    
    visualize_asrs(asrs)

if __name__ == "__main__":
    main()
