import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

class ASRSSimulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.storage = np.zeros((2, height, width), dtype=int)  # 0: empty, >0: item number
        self.crane_pos = [0, 0]  # [x, y]
        self.beat = 0
        self.operations = deque()
        self.current_operation = None

    def add_operation(self, io, item_no):
        self.operations.append((io, item_no))

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
        t_01 = 1  # Assuming 1 beat for load/unload
        t_m1 = (t_p1 + t_p2) / 2 + t_01
        t_m2 = max(points['P1'][0] + points['P2'][0], points['P1'][1] + points['P2'][1]) + t_01
        return t_m1, t_m2

    def find_empty_location(self):
        for d in range(2):
            for y in range(self.height):
                for x in range(self.width):
                    if self.storage[d, y, x] == 0:
                        return d, x, y
        return None

    def find_item_location(self, item_no):
        for d in range(2):
            for y in range(self.height):
                for x in range(self.width):
                    if self.storage[d, y, x] == item_no:
                        return d, x, y
        return None

    def move_crane(self, target_x, target_y):
        dx = target_x - self.crane_pos[0]
        dy = target_y - self.crane_pos[1]
        beats = max(abs(dx), abs(dy))
        for _ in range(beats):
            if dx != 0:
                self.crane_pos[0] += np.sign(dx)
            if dy != 0:
                self.crane_pos[1] += np.sign(dy)
            self.beat += 1
            yield self.get_state()

    def process_operation(self):
        if not self.current_operation and self.operations:
            self.current_operation = self.operations.popleft()

        if self.current_operation:
            io, item_no = self.current_operation
            if io == 1:  # Store
                location = self.find_empty_location()
                if location:
                    d, x, y = location
                    yield from self.move_crane(x, y)
                    self.storage[d, y, x] = item_no
                    self.beat += 1  # Time to store the item
                    self.current_operation = None
                    yield self.get_state()
            elif io == -1:  # Retrieve
                location = self.find_item_location(item_no)
                if location:
                    d, x, y = location
                    yield from self.move_crane(x, y)
                    self.storage[d, y, x] = 0
                    self.beat += 1  # Time to retrieve the item
                    self.current_operation = None
                    yield self.get_state()

    def get_state(self):
        return {
            'storage': self.storage.copy(),
            'crane_pos': self.crane_pos.copy(),
            'beat': self.beat,
            'current_operation': self.current_operation,
            'operations_left': len(self.operations)
        }

    def run_simulation(self):
        while self.operations or self.current_operation:
            yield from self.process_operation()

def visualize_asrs(asrs):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('AS/RS Simulation')

    def init():
        ax1.clear()
        ax2.clear()
        ax1.set_title('Storage Visualization')
        ax2.set_title('FEM9.851 Points')
        return []

    def update(state):
        ax1.clear()
        ax2.clear()
        ax1.set_title('Storage Visualization')
        ax2.set_title('FEM9.851 Points')

        # Visualize storage
        for d in range(2):
            for y in range(asrs.height):
                for x in range(asrs.width):
                    if state['storage'][d, y, x] != 0:
                        color = 'red' if d == 0 else 'blue'
                        ax1.add_patch(plt.Rectangle((x + d * (asrs.width + 1), y), 1, 1, fill=True, color=color))

        # Visualize crane
        ax1.add_patch(plt.Circle((state['crane_pos'][0] + 0.5, state['crane_pos'][1] + 0.5), 0.3, fill=True, color='green'))

        ax1.set_xlim(0, 2 * asrs.width + 1)
        ax1.set_ylim(0, asrs.height)
        ax1.invert_yaxis()

        # Visualize FEM9.851 points
        fem_points = asrs.fem_points()
        for point, (x, y) in fem_points.items():
            ax2.add_patch(plt.Circle((x, y), 0.1, fill=True, color='red'))
            ax2.annotate(point, (x, y), xytext=(5, 5), textcoords='offset points')

        ax2.set_xlim(0, asrs.width)
        ax2.set_ylim(0, asrs.height)
        ax2.invert_yaxis()

        # Display statistics
        plt.figtext(0.02, 0.02, f"Beat: {state['beat']}", fontsize=10)
        plt.figtext(0.02, 0.06, f"Current Operation: {state['current_operation']}", fontsize=10)
        plt.figtext(0.02, 0.10, f"Operations Left: {state['operations_left']}", fontsize=10)

        return []

    ani = FuncAnimation(fig, update, frames=asrs.run_simulation, init_func=init, blit=True, interval=200, repeat=False)
    plt.show()

# Example usage
asrs = ASRSSimulation(width=8, height=6)
asrs.add_operation(1, 1)  # Store item 1
asrs.add_operation(1, 2)  # Store item 2
asrs.add_operation(-1, 1)  # Retrieve item 1
asrs.add_operation(1, 3)  # Store item 3

visualize_asrs(asrs)

# Calculate and print FEM9.851 times
t_m1, t_m2 = asrs.calculate_fem_times()
print(f"FEM9.851 Single Cycle Time (t_m1): {t_m1}")
print(f"FEM9.851 Combined Cycle Time (t_m2): {t_m2}")
