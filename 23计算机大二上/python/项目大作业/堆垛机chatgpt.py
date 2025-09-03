import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
from collections import deque
from numba import jit
import warnings
import time

class ASRSSimulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.storage = np.zeros((2, height, width), dtype=np.int8)  # 货堆资源，二维存储：左侧和右侧
        self.crane_pos = np.array([0, 0], dtype=np.int8)  # 垛机位置
        self.beat = 0  # 节拍计数
        self.operations = deque()  # 出入库操作队列
        self.current_operation = None
        self.total_operations = 0
        self.completed_operations = 0

    def add_operation(self, io, item_no):
        self.operations.append((io, item_no))
        self.total_operations += 1

    def fem_points(self):
        """ 返回FEM9.851标准中的关键点E, P1, P2 """
        return {
            'E': (0, 0),  # 起点
            'P1': (self.width // 5, 2 * self.height // 3),  # P1位置
            'P2': (2 * self.width // 3, self.height // 5)   # P2位置
        }

    def calculate_fem_times(self):
        """ 计算FEM9.851标准的单循环（tm1）和组合循环（tm2）时间 """
        points = self.fem_points()
        t_p1 = max(points['P1'][0], points['P1'][1])
        t_p2 = max(points['P2'][0], points['P2'][1])
        t_01 = 1  # 额外处理时间（取货/存货）
        t_m1 = 0.5 * (t_p1 + t_p2) + t_01
        t_m2 = 2 * max(points['P1'][0], points['P2'][0]) + 2 * max(points['P1'][1], points['P2'][1]) + t_01
        return t_m1, t_m2

    @staticmethod
    @jit(nopython=True)
    def find_locations(storage, target):
        """ 查找目标位置，返回该位置的坐标 """
        return np.argwhere(storage == target)

    def find_empty_location(self):
        """ 找到一个空闲位置 """
        empty_locations = self.find_locations(self.storage, 0)
        return tuple(empty_locations[np.random.randint(len(empty_locations))]) if len(empty_locations) > 0 else None

    def find_item_location(self, item_no):
        """ 根据货物编号找到对应的货物位置 """
        locations = self.find_locations(self.storage, item_no)
        return tuple(locations[0]) if len(locations) > 0 else None

    def move_crane(self, target_x, target_y):
        """ 将堆垛机移动到目标位置，计算节拍 """
        dx = target_x - self.crane_pos[0]
        dy = target_y - self.crane_pos[1]
        steps = max(abs(dx), abs(dy))
        self.crane_pos[0] += dx
        self.crane_pos[1] += dy
        self.beat += steps

    def process_operation(self):
        """ 执行一个出入库操作 """
        if not self.current_operation and self.operations:
            self.current_operation = self.operations.popleft()

        if self.current_operation:
            io, item_no = self.current_operation
            if io == 1:  # 入库操作
                location = self.find_empty_location()
                d, y, x = location
                self.move_crane(x, y)
                self.storage[d, y, x] = item_no
                self.beat += 1
                self.move_crane(0, 0)  # 移回原点
                self.beat += 1
                self.current_operation = None
                self.completed_operations += 1
            elif io == -1:  # 出库操作
                location = self.find_item_location(item_no)
                d, y, x = location
                self.move_crane(x, y)
                self.storage[d, y, x] = 0
                self.beat += 1
                self.move_crane(0, 0)
                self.beat += 1
                self.current_operation = None
                self.completed_operations += 1

    def run_simulation(self):
        """ 运行整个模拟 """
        while self.operations or self.current_operation:
            self.process_operation()
            yield self.get_state()

    def get_state(self):
        """ 获取当前状态 """
        return {
            'storage': self.storage.copy(),
            'crane_pos': self.crane_pos.copy(),
            'beat': self.beat,
            'current_operation': self.current_operation,
            'operations_left': len(self.operations),
            'completed_operations': self.completed_operations,
            'total_operations': self.total_operations
        }

def visualize_asrs_matplotlib(asrs):
    """ 可视化堆垛机的动画过程 """
    fig, ax1 = plt.subplots(1, figsize=(15, 6))
    plt.subplots_adjust(bottom=0.3)
    fig.suptitle('AS/RS Simulation')

    ax1.set_title('Storage Visualization')

    storage_left = ax1.imshow(np.zeros((asrs.height, asrs.width)), cmap='Blues', vmin=0, vmax=1)
    storage_right = ax1.imshow(np.zeros((asrs.height, asrs.width)), cmap='Reds', vmin=0, vmax=1)
    crane, = ax1.plot([], [], 'go', markersize=10)

    ax1.set_xlim(-0.5, 2*asrs.width + 0.5)
    ax1.set_ylim(-0.5, asrs.height - 0.5)
    stats_text = ax1.text(0.02, -0.2, '', transform=ax1.transAxes, verticalalignment='top')

    def update(state):
        storage_left.set_array(state['storage'][0])
        storage_right.set_array(state['storage'][1])
        storage_right.set_extent([asrs.width, 2*asrs.width, -0.5, asrs.height-0.5])
        crane.set_data([state['crane_pos'][0]], [state['crane_pos'][1]])

        stats = f"Beat: {state['beat']}\n"
        stats += f"Current Operation: {state['current_operation']}\n"
        stats += f"Operations Left: {state['operations_left']}\n"
        stats += f"Completed: {state['completed_operations']}/{state['total_operations']}"
        stats_text.set_text(stats)

        return storage_left, storage_right, crane, stats_text

    ani = FuncAnimation(fig, update, frames=asrs.run_simulation, interval=50, repeat=False, blit=True)
    plt.show()

def generate_random_operations(max_item_no):
    """ 随机生成出入库操作 """
    return random.choice([1, -1]), random.randint(1, max_item_no)

if __name__ == "__main__":
    warnings.filterwarnings('ignore', message="NumPy will stop allowing conversion of out-of-bound Python integers to integer arrays.")
    width, height = 200, 80
    asrs = ASRSSimulation(width, height)

    max_item_no = 1000
    while True:
        user_input = input("输入 'exit' 以结束循环: ")
        if user_input == 'exit':
            break
        io, item_no = generate_random_operations(max_item_no)
        if io == 1:
            if asrs.find_empty_location() is None:
                continue
        elif io == -1:
            if asrs.find_item_location(item_no) is None:
                continue
        asrs
