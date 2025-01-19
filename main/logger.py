import json
from datetime import datetime
import os

class CoordinateLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create a new log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(log_dir, f"coordinate_log_{timestamp}.txt")
        
        # Initialize the log file with headers
        with open(self.log_file, 'w') as f:
            f.write("Timestamp,Raw_Accel_X,Raw_Accel_Y,Raw_Accel_Z,")
            f.write("Raw_Gyro_X,Raw_Gyro_Y,Raw_Gyro_Z,")
            f.write("Calc_Pos_X,Calc_Pos_Y,Calc_Pos_Z\n")

    def log_coordinates(self, raw_data, calculated_position):
        """
        Log both raw sensor data and calculated position
        raw_data: Dictionary containing accelerometer and gyroscope data
        calculated_position: Tuple of (x, y, z) calculated position
        """
        try:
            timestamp = raw_data.get('timestamp', datetime.now().timestamp())
            
            log_entry = (
                f"{timestamp},"
                f"{raw_data['accel']['x']},{raw_data['accel']['y']},{raw_data['accel']['z']},"
                f"{raw_data['gyro']['x']},{raw_data['gyro']['y']},{raw_data['gyro']['z']},"
                f"{calculated_position[0]},{calculated_position[1]},{calculated_position[2]}\n"
            )
            
            with open(self.log_file, 'a') as f:
                f.write(log_entry)
                
        except Exception as e:
            print(f"Error logging coordinates: {e}")

    def get_log_file_path(self):
        """Return the path to the current log file"""
        return self.log_file