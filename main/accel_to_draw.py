from dataclasses import dataclass
from typing import Tuple
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
        self.velocity = np.zeros(3)
        self.position = np.zeros(3)
        self.last_timestamp = None

        # Mean accelerometer readings at rest (bias)
        self.bias = np.array([203, -300, 17690])  # Adjust based on calibration

        # Previous acceleration and velocity for trapezoidal integration
        self.last_accel = np.zeros(3)
        self.last_velocity = np.zeros(3)
        
    def add_point(self, x: float, y: float, z: float, timestamp: float) -> None:
        """Add a new acceleration point to the processor"""
        point = AccelPoint(x, y, z, timestamp)
        self.accel_history.append(point)
        self._process_point(point)

    def _process_point(self, point: AccelPoint) -> None:
        """Process a new acceleration point to update velocity and position"""
        if self.last_timestamp is None:
            self.last_timestamp = point.timestamp
            self.last_accel = np.zeros(3)
            self.last_velocity = np.zeros(3)
            return

        # Calculate time delta in seconds
        dt = (point.timestamp - self.last_timestamp) / 1000.0  # Assuming timestamp is in milliseconds
        
        # Subtract bias from raw acceleration
        accel_raw = np.array([point.x, point.y, point.z])
        accel = accel_raw - self.bias

        # Apply basic noise filtering (adjust threshold as needed)
        threshold = 1.0  # Example threshold
        if np.linalg.norm(accel) < threshold:
            accel = np.zeros(3)

        # Update velocity using trapezoidal integration
        self.velocity += 0.5 * (accel + self.last_accel) * dt

        # Update position using trapezoidal integration
        self.position += self.velocity * dt + 0.5 * (accel - self.last_accel) * dt**2

        # Update stored acceleration and velocity for next iteration
        self.last_accel = accel
        self.last_velocity = self.velocity.copy()

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
        self.velocity = np.zeros(3)
        self.position = np.zeros(3)
        self.last_timestamp = None
        self.last_accel = np.zeros(3)
        self.last_velocity = np.zeros(3)
# from dataclasses import dataclass
# from typing import List, Tuple
# import numpy as np
# from collections import deque

# @dataclass
# class AccelPoint:
#     x: float
#     y: float
#     z: float
#     timestamp: float

# class AccelerationProcessor:
#     def __init__(self, window_size: int = 10):
#         self.window_size = window_size
#         self.accel_history = deque(maxlen=window_size)
#         self.velocity = np.array([0.0, 0.0, 0.0])
#         self.position = np.array([0.0, 0.0, 0.0])
#         self.last_timestamp = None

#         #TEST
#         self.last_accel = 0
#         self.last_velocity = 0
        
#     def add_point(self, x: float, y: float, z: float, timestamp: float) -> None:
#         """Add a new acceleration point to the processor"""
#         point = AccelPoint(x, y, z, timestamp)
#         self.accel_history.append(point)
#         self._process_point(point)

#     def _process_point(self, point: AccelPoint) -> None:
#         """Process a new acceleration point to update velocity and position"""
#         if self.last_timestamp is None:
#             self.last_timestamp = point.timestamp
#             return

#         # Calculate time delta in seconds
#         dt = (point.timestamp - self.last_timestamp) / 1000.0  # Assuming timestamp is in milliseconds
        
#         # Create acceleration vector and apply basic noise filtering
#         accel = np.array([point.x, point.y, point.z])
#         if abs(np.linalg.norm(accel)) < 100:  # Basic threshold filter
#             accel = np.zeros(3)

#         # Update velocity using trapezoidal integration
#         self.velocity += accel * dt
        
#         # Apply simple velocity decay to prevent drift
#         decay_factor = 0.95
#         self.velocity *= decay_factor
        
#         # Update position
#         self.position += self.velocity * dt
        
#         # Update timestamp
#         self.last_timestamp = point.timestamp

#     def get_current_position(self) -> Tuple[float, float, float]:
#         """Get the current calculated position"""
#         return tuple(self.position)

#     def get_plot_coordinates(self) -> Tuple[float, float, float]:
#         """Get the coordinates to be plotted (with z=0 when pen is down)"""
#         x, y, z = self.position
#         # Convert z position to binary up/down state
#         plot_z = 0 if abs(z) < 1000 else 1  # Threshold for considering pen "down"
#         return (x, y, plot_z)

#     def reset(self) -> None:
#         """Reset the processor state"""
#         self.accel_history.clear()
#         self.velocity = np.array([0.0, 0.0, 0.0])
#         self.position = np.array([0.0, 0.0, 0.0])
#         self.last_timestamp = None
