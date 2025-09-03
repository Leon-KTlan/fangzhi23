import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
from collections import deque
import warnings
from datetime import datetime

class ASRSSimulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.storage = np.zeros((2, height, width), dtype=np.int16)
        self.crane_pos = np.array([0, 0, 0], dtype=np.int16)  # [side, x, y]
        self.beat = 0
        self.operations = deque()
        self.current_operation = None
        self.total_operations = 0
        self.completed_operations = 0
        self.is_paused = False

    def add_operation(self, io, item_no):
        self.operations.append((io, item_no))
        self.total_operations += 1

    def fem_points(self):
        return {
            'E': (0, 0, 0),
            'P1': (0, self.width // 5, 2 * self.height // 3),
            'P2': (1, 2 * self.width // 3, self.height // 5)
        }

    def move_crane(self, target_side, target_x, target_y):
        current_side, current_x, current_y = self.crane_pos
        dx = abs(target_x - current_x)
        dy = abs(target_y - current_y)
        side_change = int(target_side != current_side)
        steps = max(dx, dy) + side_change
        self.crane_pos = np.array([target_side, target_x, target_y], dtype=np.int16)
        self.beat += steps
        return steps

    def process_operation(self):
        if self.is_paused or not self.operations:
            return

        io, item_no = self.operations.popleft()
        if io == 1:  # Store
            location = self.find_empty_location()
            if location:
                d, y, x = location
                self.move_crane(d, x, y)
                self.storage[d, y, x] = item_no
                self.beat += 1
                self.completed_operations += 1
        elif io == -1:  # Retrieve
            location = self.find_item_location(item_no)
            if location:
                d, y, x = location
                self.move_crane(d, x, y)
                self.storage[d, y, x] = 0
                self.beat += 1
                self.completed_operations += 1

    def find_empty_location(self):
        empty_locations = np.argwhere(self.storage == 0)
        return tuple(empty_locations[np.random.randint(len(empty_locations))]) if len(empty_locations) > 0 else None

    def find_item_location(self, item_no):
        locations = np.argwhere(self.storage == item_no)
        return tuple(locations[0]) if len(locations) > 0 else None

    def run_simulation(self):
        while self.operations and not self.is_paused:
            self.process_operation()
            yield self.get_state()

    def get_state(self):
        return {
            'storage': self.storage,
            'crane_pos': self.crane_pos,
            'beat': self.beat,
            'operations_left': len(self.operations),
            'completed_operations': self.completed_operations,
            'total_operations': self.total_operations
        }

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        return self.is_paused

def visualize_asrs_matplotlib(asrs):
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(15, 8))
    plt.subplots_adjust(bottom=0.2)
    fig.suptitle('AS/RS Simulation with FEM9.851 Reference Points')

    storage_left = ax_left.imshow(np.zeros((asrs.height, asrs.width//2)), 
                                cmap='Blues', vmin=0, vmax=1, 
                                extent=[0, asrs.width//2, asrs.height, 0])
    storage_right = ax_right.imshow(np.zeros((asrs.height, asrs.width//2)), 
                                  cmap='Reds', vmin=0, vmax=1, 
                                  extent=[0, asrs.width//2, asrs.height, 0])

    crane_left, = ax_left.plot([], [], 'go', markersize=10, label='Crane')
    crane_right, = ax_right.plot([], [], 'go', markersize=10, label='Crane')

    fem_points = asrs.fem_points()
    ax_left.plot(fem_points['P1'][1], fem_points['P1'][2], 'r*', markersize=10)
    ax_right.plot(fem_points['P2'][1], fem_points['P2'][2], 'r*', markersize=10)

    ax_left.text(0, 0, 'E', fontsize=12)
    ax_left.text(fem_points['P1'][1], fem_points['P1'][2], 'P1', fontsize=12)
    ax_right.text(fem_points['P2'][1], fem_points['P2'][2], 'P2', fontsize=12)

    for ax in [ax_left, ax_right]:
        ax.set_xlim(0, asrs.width//2)
        ax.set_ylim(asrs.height, 0)
        ax.grid(True)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

    ax_left.set_title('Left Storage')
    ax_right.set_title('Right Storage')

    stats_text = fig.text(0.02, 0.02, '', transform=fig.transFigure)

    pause_ax = plt.axes([0.8, 0.025, 0.1, 0.04])
    pause_button = plt.Button(pause_ax, 'Pause/Resume')
    pause_button.on_clicked(lambda event: asrs.toggle_pause())

    def update(state):
        if state is None:
            return storage_left, storage_right, crane_left, crane_right, stats_text

        storage_left.set_array(state['storage'][0])
        storage_right.set_array(state['storage'][1])
        
        if state['crane_pos'][0] == 0:  # Left side
            crane_left.set_data([state['crane_pos'][1]], [state['crane_pos'][2]])
            crane_right.set_data([], [])
        else:  # Right side
            crane_left.set_data([], [])
            crane_right.set_data([state['crane_pos'][1]], [state['crane_pos'][2]])

        stats = (f"Beat: {state['beat']}\n"
                f"Operations Left: {state['operations_left']}\n"
                f"Completed: {state['completed_operations']}/{state['total_operations']}")
        stats_text.set_text(stats)

        return storage_left, storage_right, crane_left, crane_right, stats_text

    ani = FuncAnimation(fig, update, frames=asrs.run_simulation, 
                       interval=50, repeat=False, blit=True)
    plt.show()

def generate_random_operations(num_operations, max_item_no):
    operations = []
    current_items = set()
    
    for _ in range(num_operations):
        if len(current_items) == 0 or (len(current_items) < max_item_no and random.random() < 0.7):
            item_no = max(current_items) + 1 if current_items else 1
            current_items.add(item_no)
            operations.append((1, item_no))
        else:
            item_no = random.choice(list(current_items))
            current_items.remove(item_no)
            operations.append((-1, item_no))
            
    return operations

if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    
    width, height = 200, 80
    asrs = ASRSSimulation(width, height)
    
    num_operations = 1000
    max_item_no = 1000
    operations = generate_random_operations(num_operations, max_item_no)
    for io, item_no in operations:
        asrs.add_operation(io, item_no)
    
    visualize_asrs_matplotlib(asrs)
    
    warnings.filterwarnings('default')

