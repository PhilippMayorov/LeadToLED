from dataclasses import dataclass
import numpy as np
from typing import List, Tuple, Optional
import time

@dataclass
class SensorData:
    timestamp: float
    accel: Tuple[float, float, float]
    gyro: Tuple[float, float, float]

class PositionIntegrator:
    def __init__(self):
        # Position state
        self.position = np.zeros(3)
        self.velocity = np.zeros(3)
        self.orientation = np.eye(3)  # Rotation matrix
        
        # Calibration parameters
        self.gravity = np.array([0, 0, 9.81])
        self.accel_threshold = 0.1  # m/s²
        self.velocity_decay = 0.95  # Decay factor to prevent drift
        
        # Time tracking
        self.last_update = None
        
        # Drawing state
        self.is_drawing = False
        self.draw_points: List[Tuple[float, float, float]] = []
        
    def process_sensor_data(self, data: SensorData) -> Optional[Tuple[float, float, float]]:
        """Process new sensor data and return position if drawing"""
        current_time = data.timestamp
        
        if self.last_update is None:
            self.last_update = current_time
            return None
            
        # Calculate time delta
        dt = (current_time - self.last_update) / 1000.0  # Convert to seconds
        
        # Update orientation using gyroscope data
        self._update_orientation(data.gyro, dt)
        
        # Process acceleration
        accel = np.array(data.accel)
        accel_global = self._transform_acceleration(accel)
        
        # Update position
        self._update_position(accel_global, dt)
        
        # Update timestamp
        self.last_update = current_time
        
        # Determine if we should be drawing based on z-position
        self.is_drawing = True #abs(self.position[2]) < 0.1  # Within 10cm of surface
        
        if self.is_drawing:
            point = tuple(self.position)
            self.draw_points.append(point)
            return point
        return None
        
    def _update_orientation(self, gyro: Tuple[float, float, float], dt: float):
        """Update orientation based on gyroscope readings"""
        gyro_data = np.array(gyro)
        angle = np.linalg.norm(gyro_data) * dt
        
        if angle > 0:
            axis = gyro_data / np.linalg.norm(gyro_data)
            c = np.cos(angle)
            s = np.sin(angle)
            v = 1 - c
            
            rotation = np.array([
                [axis[0]*axis[0]*v + c, axis[0]*axis[1]*v - axis[2]*s, axis[0]*axis[2]*v + axis[1]*s],
                [axis[1]*axis[0]*v + axis[2]*s, axis[1]*axis[1]*v + c, axis[1]*axis[2]*v - axis[0]*s],
                [axis[2]*axis[0]*v - axis[1]*s, axis[2]*axis[1]*v + axis[0]*s, axis[2]*axis[2]*v + c]
            ])
            
            self.orientation = np.dot(rotation, self.orientation)
            
    def _transform_acceleration(self, accel: np.ndarray) -> np.ndarray:
        """Transform acceleration from sensor to global frame and remove gravity"""
        # Transform to global frame
        accel_global = np.dot(self.orientation, accel)
        
        # Remove gravity
        accel_global -= self.gravity
        
        # Apply threshold to reduce noise
        accel_global = np.where(np.abs(accel_global) < self.accel_threshold, 0, accel_global)
        
        return accel_global
        
    def _update_position(self, accel: np.ndarray, dt: float):
        """Update position using double integration"""
        # Update velocity (trapezoidal integration)
        self.velocity += accel * dt
        
        # Apply velocity decay to prevent drift
        self.velocity *= self.velocity_decay
        
        # Update position
        self.position += self.velocity * dt + 0.5 * accel * dt**2
        
    def get_drawing(self) -> List[Tuple[float, float, float]]:
        """Return the current drawing points"""
        return self.draw_points
        
    def reset(self):
        """Reset the integrator state"""
        self.position = np.zeros(3)
        self.velocity = np.zeros(3)
        self.orientation = np.eye(3)
        self.last_update = None
        self.draw_points.clear()
