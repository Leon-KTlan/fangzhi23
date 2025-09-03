import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
from collections import deque
from numba import jit

class ASRSSimulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.storage = np.zeros((2, height, width), dtype=np.int8)
        self.crane_pos = np.array([0, 0], dtype=np.int8)
        self.beat = 0
        self.operations = deque()
        self.current_operation = None
        self.total_operations = 0
        self.completed_operations = 0

    def add_operation(self, io, item_no):
        self.operations.append((io, item_no))
        self.total_operations += 1

    def fem_points(self):
        return {
            'E': (0, 0),
            'P1': (self.width // 5, 2 * self.height // 3),
            'P2': (2 * self.width // 3, self.height // 5)
        }

    def calculate_fem_times(self):
        points = self.fem_points()
        t_p1 = max(points['P1'][0], points['P1'][1])
        t_p2 = max(points['P2'][0], points['P2'][1])
        t_01 = 1
        t_m1 = (t_p1 + t_p2) / 2 + t_01
        t_m2 = max(points['P1'][0] + points['P2'][0], points['P1'][1] + points['P2'][1]) + t_01
        return t_m1, t_m2

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

    @staticmethod
    @jit(nopython=True)
    def move_crane_fast(crane_pos, target_x, target_y, beat):
        dx = target_x - crane_pos[0]
        dy = target_y - crane_pos[1]
        steps = max(abs(dx), abs(dy))
        for _ in range(steps):
            if dx != 0:
                crane_pos[0] += np.sign(dx)
            if dy != 0:
                crane_pos[1] += np.sign(dy)
            beat += 1
        return crane_pos, beat

    def move_crane(self, target_x, target_y):
        self.crane_pos, self.beat = self.move_crane_fast(self.crane_pos, target_x, target_y, self.beat)

    def process_operation(self):
        if not self.current_operation and self.operations:
            self.current_operation = self.operations.popleft()

        if self.current_operation:
            io, item_no = self.current_operation
            if io == 1:  # Store
                location = self.find_empty_location()
                if location:
                    d, y, x = location
                    self.move_crane(x, y)
                    self.storage[d, y, x] = item_no
                    self.beat += 1
                    self.current_operation = None
                    self.completed_operations += 1
            elif io == -1:  # Retrieve
                location = self.find_item_location(item_no)
                if location:
                    d, y, x = location
                    self.move_crane(x, y)
                    self.storage[d, y, x] = 0
                    self.beat += 1
                    self.current_operation = None
                    self.completed_operations += 1

    def run_simulation(self):
        while self.operations or self.current_operation:
            self.process_operation()
            yield self.get_state()

    def get_state(self):
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
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    plt.subplots_adjust(bottom=0.3)
    fig.suptitle('AS/RS Simulation')

    ax1.set_title('Storage Visualization')
    ax2.set_title('FEM9.851 Points')

    storage_left = ax1.imshow(np.zeros((asrs.height, asrs.width)), cmap='Blues', vmin=0, vmax=1)
    storage_right = ax1.imshow(np.zeros((asrs.height, asrs.width)), cmap='Reds', vmin=0, vmax=1)
    crane, = ax1.plot([], [], 'go', markersize=10)

    ax1.set_xlim(-0.5, 2 * asrs.width + 0.5)
    ax1.set_ylim(-0.5, asrs.height - 0.5)
    ax1.invert_yaxis()

    fem_points = asrs.fem_points()
    for point, (x, y) in fem_points.items():
        ax2.plot(x, y, 'ro')
        ax2.annotate(point, (x, y), xytext=(5, 5), textcoords='offset points')

    ax2.set_xlim(0, asrs.width)
    ax2.set_ylim(0, asrs.height)
    ax2.invert_yaxis()

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

def generate_random_operations(num_operations, max_item_no):
    return [(random.choice([1, -1]), random.randint(1, max_item_no)) for _ in range(num_operations)]

if __name__ == "__main__":
    width, height = 8, 6
    asrs = ASRSSimulation(width, height)

    num_operations = 100
    max_item_no = 10
    random_operations = generate_random_operations(num_operations, max_item_no)

    for io, item_no in random_operations:
        asrs.add_operation(io, item_no)

    visualize_asrs_matplotlib(asrs)

    t_m1, t_m2 = asrs.calculate_fem_times()
    print(f"FEM9.851 Single Cycle Time (t_m1): {t_m1}")
    print(f"FEM9.851 Combined Cycle Time (t_m2): {t_m2}")

    total_beats = asrs.beat
    total_operations = asrs.completed_operations
    average_cycle_time = total_beats / total_operations if total_operations > 0 else 0
    print(f"Actual Average Cycle Time: {average_cycle_time:.2f}")
    print(f"Difference from t_m1: {average_cycle_time - t_m1:.2f}")
    print(f"Difference from t_m2: {average_cycle_time - t_m2:.2f}")
