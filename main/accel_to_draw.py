from dataclasses import dataclass
from typing import Tuple
import numpy as np
from collections import deque

@dataclass
class IMUPoint:
    # Accelerometer data (m/s²)
    ax: float
    ay: float
    az: float
    # Gyroscope data (rad/s)
    gx: float
    gy: float
    gz: float
    timestamp: float

class MotionProcessor:
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.imu_history = deque(maxlen=window_size)
        
        # Motion states
        self.velocity = np.zeros(3)
        self.position = np.zeros(3)
        self.orientation = np.eye(3)  # Rotation matrix
        
        # Timing
        self.last_timestamp = None
        
        # Previous states for integration
        self.last_accel = np.zeros(3)
        self.last_gyro = np.zeros(3)
        self.last_velocity = np.zeros(3)
        
        # Calibration parameters
        self.accel_bias = np.array([203, -300, 17690])  # Adjust based on calibration
        self.gyro_bias = np.array([0, 0, 0])  # Adjust based on calibration
        
        # Filter parameters
        self.accel_threshold = 1.0
        self.gyro_threshold = 0.1
        
    def add_point(self, ax: float, ay: float, az: float, 
                 gx: float, gy: float, gz: float, timestamp: float) -> None:
        """Add a new IMU measurement"""
        point = IMUPoint(ax, ay, az, gx, gy, gz, timestamp)
        self.imu_history.append(point)
        self._process_point(point)

    def _process_point(self, point: IMUPoint) -> None:
        """Process new IMU data to update position and orientation"""
        if self.last_timestamp is None:
            self.last_timestamp = point.timestamp
            return

        # Calculate time delta in seconds
        dt = (point.timestamp - self.last_timestamp) / 1000.0
        
        # Process accelerometer data
        accel_raw = np.array([point.ax, point.ay, point.az])
        accel = accel_raw - self.accel_bias
        
        # Process gyroscope data
        gyro_raw = np.array([point.gx, point.gy, point.gz])
        gyro = gyro_raw - self.gyro_bias
        
        # Apply noise thresholds
        accel = np.where(np.abs(accel) < self.accel_threshold, 0, accel)
        gyro = np.where(np.abs(gyro) < self.gyro_threshold, 0, gyro)
        
        # Update orientation using gyroscope data
        angle = np.linalg.norm(gyro) * dt
        if angle > 0:
            axis = gyro / np.linalg.norm(gyro)
            c = np.cos(angle)
            s = np.sin(angle)
            v = 1 - c
            
            # Rodriguez rotation formula
            rotation = np.array([
                [axis[0]*axis[0]*v + c, axis[0]*axis[1]*v - axis[2]*s, axis[0]*axis[2]*v + axis[1]*s],
                [axis[1]*axis[0]*v + axis[2]*s, axis[1]*axis[1]*v + c, axis[1]*axis[2]*v - axis[0]*s],
                [axis[2]*axis[0]*v - axis[1]*s, axis[2]*axis[1]*v + axis[0]*s, axis[2]*axis[2]*v + c]
            ])
            
            self.orientation = np.dot(rotation, self.orientation)
        
        # Transform acceleration to global frame
        accel_global = np.dot(self.orientation, accel)
        
        # Remove gravity
        gravity = np.array([0, 0, 9.81])
        accel_global -= gravity
        
        # Update velocity using trapezoidal integration
        self.velocity += 0.5 * (accel_global + self.last_accel) * dt
        
        # Apply velocity decay to prevent drift
        decay_factor = 0.95
        self.velocity *= decay_factor
        
        # Update position using trapezoidal integration
        self.position += self.velocity * dt + 0.5 * accel_global * dt**2
        
        # Store current values for next iteration
        self.last_accel = accel_global
        self.last_gyro = gyro
        self.last_timestamp = point.timestamp

    def get_current_position(self) -> Tuple[float, float, float]:
        """Get the current calculated position"""
        return tuple(self.position)

    def get_plot_coordinates(self) -> Tuple[float, float, float]:
        """Get the coordinates to be plotted (with z=0 when pen is down)"""
        x, y, z = self.position
        plot_z = 0 if abs(z) < 1000 else 1
        return (x, y, plot_z)

    def reset(self) -> None:
        """Reset the processor state"""
        self.imu_history.clear()
        self.velocity = np.zeros(3)
        self.position = np.zeros(3)
        self.orientation = np.eye(3)
        self.last_timestamp = None
        self.last_accel = np.zeros(3)
        self.last_gyro = np.zeros(3)
        self.last_velocity = np.zeros(3)