# mqtt_handler.py
import paho.mqtt.client as mqtt
import json
import configparser
from accel_to_draw import AccelerationProcessor

class MQTTHandler:
    def __init__(self, mongo_handler=None, plotter=None, config_path='config.properties'):
        """
        Initialize MQTT Handler
        mongo_handler: Optional MongoDB handler for storing coordinates
        plotter: Optional Plotter instance for visualization
        """
        self.config = self._load_config(config_path)
        self.mongo_handler = mongo_handler
        self.plotter = plotter
        self.client = None
        # Initialize the acceleration processor
        self.accel_processor = AccelerationProcessor()
        
        # Store local acceleration and gyro data
        self.current_accel = {'x': 0, 'y': 0, 'z': 0}
        self.current_gyro = {'x': 0, 'y': 0, 'z': 0}

    def _load_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        return {
            'host': config.get('mqtt', 'host'),
            'port': config.getint('mqtt', 'port'),
            'username': config.get('mqtt', 'username'),
            'password': config.get('mqtt', 'password')
        }

    def on_connect(self, client, userdata, flags, reason_code, properties=None):
        print(f"Connected with result code {reason_code}")
        client.subscribe("coordinates", qos=1)

    def on_message(self, client, userdata, message):
        try:
            data = json.loads(message.payload.decode())
            print(f"Received sensor data:")
            print(f"Accelerometer: ({data['accel']['x']}, {data['accel']['y']}, {data['accel']['z']})")
            print(f"Gyroscope: ({data['gyro']['x']}, {data['gyro']['y']}, {data['gyro']['z']})")
            print(f"Timestamp: {data['timestamp']}")
            
            # Update local storage
            self.current_accel = data['accel']
            self.current_gyro = data['gyro']
            
            # Process acceleration data to get position
            self.accel_processor.add_point(
                self.current_accel['x'],
                self.current_accel['y'],
                self.current_accel['z'],
                data['timestamp'],
                # gyro_x=self.current_gyro['x'],
                # gyro_y=self.current_gyro['y'],
                # gyro_z=self.current_gyro['z']
            )
            
            # Get the current position
            x, y, z = self.accel_processor.get_plot_coordinates()
            print(f"Calculated position: ({x}, {y}, {z})")
            
            # Add to plotter if available
            if self.plotter:
                self.plotter.add_point(x, y, z)

            # Store in MongoDB if handler available
            if self.mongo_handler:
                self.mongo_handler.insert_coordinates(
                    accel_data=self.current_accel,
                    gyro_data=self.current_gyro,
                    timestamp=data['timestamp']
                )

            if z == 0:
                print("Point will be plotted (z=0)")
            else:
                print("Point will be skipped (z≠0)")
            print("-------------------")
            
        except Exception as e:
            print(f"Error processing message: {e}")

    def connect(self):
        """Establish MQTT connection"""
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        # Set credentials
        self.client.username_pw_set(self.config['username'], self.config['password'])
        
        # Enable SSL/TLS
        self.client.tls_set()
        
        # Connect to Solace Cloud
        try:
            self.client.connect(self.config['host'], self.config['port'], 60)
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def start(self):
        """Start MQTT client loop"""
        if self.client:
            self.client.loop_start()

    def stop(self):
        """Stop MQTT client"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()