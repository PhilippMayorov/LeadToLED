from dataclasses import dataclass
from typing import List, Tuple
import numpy as np
from collections import deque

@dataclass
class AccelPoint:
    x: float
    y: float
    z: float
    timestamp: float

class AccelerationProcessor:
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.accel_history = deque(maxlen=window_size)
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.position = np.array([0.0, 0.0, 0.0])
        self.last_timestamp = None
        
    def add_point(self, x: float, y: float, z: float, timestamp: float) -> None:
        """Add a new acceleration point to the processor"""
        point = AccelPoint(x, y, z, timestamp)
        self.accel_history.append(point)
        self._process_point(point)

    def _process_point(self, point: AccelPoint) -> None:
        """Process a new acceleration point to update velocity and position"""
        if self.last_timestamp is None:
            self.last_timestamp = point.timestamp
            return

        # Calculate time delta in seconds
        dt = (point.timestamp - self.last_timestamp) / 1000.0  # Assuming timestamp is in milliseconds
        
        # Create acceleration vector and apply basic noise filtering
        accel = np.array([point.x, point.y, point.z])
        if abs(np.linalg.norm(accel)) < 100:  # Basic threshold filter
            accel = np.zeros(3)

        # Update velocity using trapezoidal integration
        self.velocity += accel * dt
        
        # Apply simple velocity decay to prevent drift
        decay_factor = 0.95
        self.velocity *= decay_factor
        
        # Update position
        self.position += self.velocity * dt
        
        # Update timestamp
        self.last_timestamp = point.timestamp

    def get_current_position(self) -> Tuple[float, float, float]:
        """Get the current calculated position"""
        return tuple(self.position)

    def get_plot_coordinates(self) -> Tuple[float, float, float]:
        """Get the coordinates to be plotted (with z=0 when pen is down)"""
        x, y, z = self.position
        # Convert z position to binary up/down state
        plot_z = 0 if abs(z) < 1000 else 1  # Threshold for considering pen "down"
        return (x, y, plot_z)

    def reset(self) -> None:
        """Reset the processor state"""
        self.accel_history.clear()
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.position = np.array([0.0, 0.0, 0.0])
        self.last_timestamp = None
