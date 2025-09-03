import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.font_manager as fm
import random
from collections import deque

# Set up a font that supports Chinese characters
plt.rcParams['font.sans-serif'] = ['SimHei']  # Use SimHei font for Chinese characters
plt.rcParams['axes.unicode_minus'] = False  # Ensure minus sign is displayed correctly

class ASRSSimulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.storage = np.zeros((2, height, width), dtype=np.int16)
        self.crane_pos = [0, 0, 0]  # [side, x, y]
        self.beat = 0
        self.operations = deque()
        self.total_operations = 0
        self.completed_operations = 0
        
        self.p1_pos = [self.width // 5, 2 * self.height // 3]
        self.p2_pos = [2 * self.width // 3, self.height // 5]
        
        self.current_path = []
        self.is_loading = False
        self.current_operation = None

    def add_operation(self, io, item_no):
        self.operations.append((io, item_no))
        self.total_operations += 1

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
        if not self.current_path and not self.is_loading:
            if self.operations:
                io, item_no = self.operations.popleft()
                if io == 1:  # Store
                    target = [0, self.p1_pos[0], self.p1_pos[1]]
                else:  # Retrieve
                    target = [1, self.p2_pos[0], self.p2_pos[1]]
                self.current_path = self.calculate_path(self.crane_pos, target)
                self.current_operation = (io, item_no)
            else:
                return False

        if self.current_path:
            self.crane_pos = self.current_path.pop(0)
            self.beat += 1
        elif not self.is_loading:
            self.is_loading = True
            self.beat += 1
        else:
            self.is_loading = False
            self.completed_operations += 1
            self.current_operation = None
            self.current_path = self.calculate_path(self.crane_pos, [0, 0, 0])

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

    ax1.plot(asrs.p1_pos[0], asrs.p1_pos[1], 'r*', markersize=10, label='P1')
    ax2.plot(asrs.p2_pos[0], asrs.p2_pos[1], 'r*', markersize=10, label='P2')

    stats_text = ax1.text(0.02, -0.2, '', transform=ax1.transAxes)

    def update(frame):
        if not asrs.step():
            return []

        state = asrs.get_state()
        
        storage_left.set_array(state['storage'][0])
        storage_right.set_array(state['storage'][1])

        if state['crane_pos'][0] == 0:
            crane_left.set_data([state['crane_pos'][1]], [state['crane_pos'][2]])
            crane_right.set_data([], [])
        else:
            crane_left.set_data([], [])
            crane_right.set_data([state['crane_pos'][1]], [state['crane_pos'][2]])

        stats = (f"节拍数: {state['beat']}\n"
                f"剩余操作: {state['operations_left']}\n"
                f"已完成: {state['completed_operations']}/{state['total_operations']}\n"
                f"状态: {'装卸货中' if state['is_loading'] else '移动中'}")
        stats_text.set_text(stats)

        return [storage_left, storage_right, crane_left, crane_right, stats_text]

    ani = FuncAnimation(fig, update, frames=None, 
                       interval=100, repeat=False, save_count=1000)
    plt.show()

def main():
    width, height = 50, 80
    asrs = ASRSSimulation(width, height)
    
    num_operations = 20
    for _ in range(num_operations):
        io = random.choice([1, -1])
        item_no = random.randint(1, 100)
        asrs.add_operation(io, item_no)
    
    visualize_asrs(asrs)

if __name__ == "__main__":
    main()
