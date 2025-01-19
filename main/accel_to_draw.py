
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
        # Motion states
        self.position = np.zeros(3)
        
        # Base values (from your stationary data)
        self.accel_offset = np.array([-1950, 100, 17600])
        
        # Movement parameters
        self.movement_speed = 50.0
        self.rest_threshold = 200
        
        # Calibration state
        self.is_calibrating = True
        self.calibration_samples_x = deque(maxlen=20)  # Reduced sample size for quicker updates
        self.calibration_samples_y = deque(maxlen=20)
        self.accel_threshold_x = 250  # Initial values
        self.accel_threshold_y = 650
        
        # State tracking
        self.is_moving = False
        self.current_direction = np.zeros(3)
        self.rest_samples = deque(maxlen=8)
        self.last_timestamp = None
        
        # Add Y-axis stability tracking
        self.y_samples = deque(maxlen=3)

    def _update_thresholds(self, accel):
        """Update thresholds based on current rest period readings"""
        self.calibration_samples_x.append(accel[0])
        self.calibration_samples_y.append(accel[1])
        
        if len(self.calibration_samples_x) >= 10:  # Wait for at least 10 samples
            x_std = np.std(self.calibration_samples_x)
            y_std = np.std(self.calibration_samples_y)
            
            # Update X threshold (with bounds)
            self.accel_threshold_x = max(250, min(500, x_std * 3.0))
            
            # Update Y threshold (with bounds)
            self.accel_threshold_y = max(500, min(800, y_std * 3.0))
            
            print(f"Updated thresholds - X: {self.accel_threshold_x:.1f}, Y: {self.accel_threshold_y:.1f}")

    def _is_at_rest(self, accel_raw):
        """Determine if sensor is at rest"""
        accel_diff = np.abs(accel_raw - self.accel_offset)
        is_rest = np.all(accel_diff < self.rest_threshold)
        self.rest_samples.append(is_rest)
        return len(self.rest_samples) >= 3 and all(self.rest_samples)

    def _is_y_stable(self, accel_y):
        """Check if Y acceleration is stable"""
        self.y_samples.append(accel_y)
        if len(self.y_samples) < 3:
            return False
        y_variation = np.std(self.y_samples)
        return y_variation < 200

    def _process_point(self, point: IMUPoint) -> None:
        if self.last_timestamp is None:
            self.last_timestamp = point.timestamp
            return

        dt = (point.timestamp - self.last_timestamp) / 1000.0
        accel_raw = np.array([point.ax, point.ay, point.az])
        
        # Get acceleration relative to baseline
        accel = accel_raw - self.accel_offset
        
        # Check if at rest
        if self._is_at_rest(accel_raw):
            if self.is_moving:  # Just came to rest
                self.calibration_samples_x.clear()
                self.calibration_samples_y.clear()
            
            self.is_moving = False
            self.current_direction = np.zeros(3)
            self._update_thresholds(accel)  # Update thresholds during rest
            self.last_timestamp = point.timestamp
            return

        # If not moving, check for start of movement
        if not self.is_moving:
            # First check Y-axis movement
            if abs(accel[1]) > self.accel_threshold_y:
                self.is_moving = True
                self.current_direction = np.zeros(3)
                self.current_direction[1] = -np.sign(accel[1])
            # Only check X-axis if Y is stable
            elif self._is_y_stable(accel[1]) and abs(accel[0]) > self.accel_threshold_x:
                self.is_moving = True
                self.current_direction = np.zeros(3)
                self.current_direction[0] = -np.sign(accel[0])

        # If moving, update position based on current direction
        if self.is_moving:
            self.position += self.current_direction * self.movement_speed * dt

        self.last_timestamp = point.timestamp

    def add_point(self, ax: float, ay: float, az: float, 
                 gx: float, gy: float, gz: float, timestamp: float) -> None:
        point = IMUPoint(ax, ay, az, gx, gy, gz, timestamp)
        self._process_point(point)

    def get_current_position(self) -> Tuple[float, float, float]:
        return tuple(self.position)

    def get_plot_coordinates(self) -> Tuple[float, float, float]:
        x, y, z = self.position
        return (x, y, 0 if self.is_moving else 1)

    def reset(self) -> None:
        self.__init__(10)