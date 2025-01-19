# plotter.py
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import numpy as np
from queue import Queue
from threading import Lock

class Plotter:
    def __init__(self, max_points=100):
        # Initialize deques for storing coordinates
        self.x_coords = deque(maxlen=max_points)
        self.y_coords = deque(maxlen=max_points)
        self.z_coords = deque(maxlen=max_points)
        
        # Thread-safe queue for new points
        self.point_queue = Queue()
        self.lock = Lock()
        
        # Set up the plot
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111)
        self.lines = []
        self.animation = None
        
        # Initialize the plot
        self._setup_plot()

    def _setup_plot(self):
        """Initialize plot settings"""
        self.ax.set_title('Coordinate Tracking (Z=0 only)')
        self.ax.set_xlabel('Y Coordinate (Longitude)')
        self.ax.set_ylabel('X Coordinate (Latitude)')
        self.ax.grid(True)

    def add_point(self, x, y, z):
        """Add a single coordinate point to queue"""
        self.point_queue.put((x, y, z))

    def add_points(self, coordinates):
        """Add multiple coordinate points for animation"""
        # Clear existing points
        self.clear()
        
        # Store coordinates for animation
        self.coordinate_list = coordinates
        self.current_index = 0

    def _process_queue(self):
        """Process any points in the queue"""
        while not self.point_queue.empty():
            with self.lock:
                x, y, z = self.point_queue.get()
                self.x_coords.append(x)
                self.y_coords.append(y)
                self.z_coords.append(z)

    def _update_plot(self, frame):
        """Update function for animation"""
        # Process any new points in the queue
        self._process_queue()

        # Clear previous lines
        for line in self.lines:
            line.remove()
        self.lines.clear()
        
        if len(self.x_coords) > 0:
            # Create segments of continuous z=0 points
            segments_x = []
            segments_y = []
            current_segment_x = []
            current_segment_y = []
            
            # Group continuous z=0 points into segments
            for x, y, z in zip(self.x_coords, self.y_coords, self.z_coords):
                if z == 0:
                    current_segment_x.append(x)
                    current_segment_y.append(y)
                else:
                    if current_segment_x:
                        segments_x.append(current_segment_x)
                        segments_y.append(current_segment_y)
                        current_segment_x = []
                        current_segment_y = []
            
            # Add the last segment if it exists
            if current_segment_x:
                segments_x.append(current_segment_x)
                segments_y.append(current_segment_y)
            
            # Plot each segment
            for seg_x, seg_y in zip(segments_x, segments_y):
                line, = self.ax.plot(seg_y, seg_x, 'b-')
                self.lines.append(line)
                
                # Add point at the end of each segment
                point, = self.ax.plot([seg_y[-1]], [seg_x[-1]], 'ro')
                self.lines.append(point)
            
            # Adjust plot limits
            self.ax.relim()
            self.ax.autoscale_view()
        
        return self.lines

    def _animate(self, frame):
        """Animation function for multiple points"""
        if hasattr(self, 'coordinate_list') and self.current_index < len(self.coordinate_list):
            coord = self.coordinate_list[self.current_index]
            if isinstance(coord, dict):
                self.add_point(coord['x'], coord['y'], coord['z'])
            else:
                self.add_point(coord[0], coord[1], coord[2])
            self.current_index += 1
        return self._update_plot(frame)

    def start_animation(self, interval=100):
        """Start animation"""
        self.animation = FuncAnimation(
            self.fig,
            self._update_plot,
            interval=interval,
            blit=True
        )
        plt.show()

    def plot_static(self):
        """Create a static plot of current coordinates"""
        self._update_plot(None)
        plt.show()

    def clear(self):
        """Clear all coordinates"""
        with self.lock:
            self.x_coords.clear()
            self.y_coords.clear()
            self.z_coords.clear()
            while not self.point_queue.empty():
                self.point_queue.get()