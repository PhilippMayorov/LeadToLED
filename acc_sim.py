import paho.mqtt.client as mqtt
import json
import time
import math
import random
import configparser

# Add program start time
PROGRAM_START_TIME = time.time() * 1000  # Convert to milliseconds

# Load configuration
def load_config():
    config = configparser.ConfigParser()
    config.read('config.properties')
    return {
        'host': config.get('mqtt', 'host'),
        'port': config.getint('mqtt', 'port'),
        'username': config.get('mqtt', 'username'),
        'password': config.get('mqtt', 'password'),
    }

config = load_config()

# Use configuration values
MQTT_HOST = config['host']
MQTT_PORT = config['port']
MQTT_USER = config['username']
MQTT_PASSWORD = config['password']

# Track time since last reset
last_reset_time = time.time()
RESET_INTERVAL = random.uniform(2, 6)  # Random interval between 2 and 6 seconds

# Constants for acceleration calculation
ANGULAR_VELOCITY = 20.0  # radians per second
CIRCLE_RADIUS = 10.0    # meters

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected with result code {reason_code}")

def should_reset():
    global last_reset_time, RESET_INTERVAL
    current_time = time.time()
    if current_time - last_reset_time >= RESET_INTERVAL:
        last_reset_time = current_time
        RESET_INTERVAL = random.uniform(5, 15)  # Set new random interval
        return True
    return False

def simulate_circular_acceleration():
    global last_reset_time
    
    # Check if it's time to reset
    if should_reset():
        acceleration = {
            "x": "-",
            "y": "-",
            "z": "-",
            "timestamp": int(time.time() * 1000 - PROGRAM_START_TIME)
        }
        print("Canvas Reset Signal Sent")
        return acceleration
    
    # Calculate current angle
    current_time = time.time()
    angle = (current_time * ANGULAR_VELOCITY) % (2 * math.pi)
    
    # Calculate centripetal acceleration components
    # a = ω²r where ω is angular velocity and r is radius
    centripetal_acceleration = ANGULAR_VELOCITY ** 2 * CIRCLE_RADIUS
    
    # Break down acceleration into x and y components
    # x-axis acceleration
    ax = centripetal_acceleration * math.cos(angle)
    # y-axis acceleration
    ay = centripetal_acceleration * math.sin(angle)
    
    # Add some noise to make it more realistic
    noise_factor = 0.1
    ax += random.uniform(-noise_factor, noise_factor)
    ay += random.uniform(-noise_factor, noise_factor)
    
    # Randomly decide to add vertical acceleration (z-axis)
    az = random.uniform(-0.5, 0.5) if random.random() < 0.2 else 0
    
    # Convert to g-forces (1g = 9.81 m/s²)
    ax_g = ax / 9.81
    ay_g = ay / 9.81
    az_g = az / 9.81
    
    acceleration = {
        "x": round(ax_g, 3),
        "y": round(ay_g, 3),
        "z": round(az_g, 3),
        "timestamp": int(time.time() * 1000 - PROGRAM_START_TIME)
    }
    
    # Print acceleration values
    print(f"Acceleration (g): x={ax_g:.3f}, y={ay_g:.3f}, z={az_g:.3f}")
    
    return acceleration

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    
    # Set credentials
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    
    # Enable SSL/TLS
    client.tls_set()
    
    # Connect to Solace Cloud
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    
    # Start the MQTT client loop in the background
    client.loop_start()
    
    try:
        while True:
            acceleration_data = simulate_circular_acceleration()
            topic = "coordinates"  # Changed topic to reflect acceleration data
            client.publish(topic, json.dumps(acceleration_data), qos=1, retain=False)
            print(f"Published: {acceleration_data}")
            print(f"Time until next reset: {RESET_INTERVAL - (time.time() - last_reset_time):.1f} seconds")
            print("-------------------")
            time.sleep(0.1)  # Smaller sleep time for smoother data
            
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
# import paho.mqtt.client as mqtt
# import json
# import time
# import math
# import random
# from datetime import datetime
# import configparser

# # Load configuration
# def load_config():
#     config = configparser.ConfigParser()
#     config.read('config.properties')
#     return {
#         'host': config.get('mqtt', 'host'),
#         'port': config.getint('mqtt', 'port'),
#         'username': config.get('mqtt', 'username'),
#         'password': config.get('mqtt', 'password'),
#     }

# config = load_config()

# # Use configuration values
# MQTT_HOST = config['host']
# MQTT_PORT = config['port']
# MQTT_USER = config['username']
# MQTT_PASSWORD = config['password']

# # Track time since last reset
# last_reset_time = time.time()
# RESET_INTERVAL = random.uniform(2, 6)  # Random interval between 5 and 15 seconds

# def on_connect(client, userdata, flags, reason_code, properties=None):
#     print(f"Connected with result code {reason_code}")

# def should_reset():
#     global last_reset_time, RESET_INTERVAL
#     current_time = time.time()
#     if current_time - last_reset_time >= RESET_INTERVAL:
#         last_reset_time = current_time
#         RESET_INTERVAL = random.uniform(5, 15)  # Set new random interval
#         return True
#     return False

# def simulate_circular_movement():
#     global last_reset_time
    
#     # Check if it's time to reset
#     if should_reset():
#         coordinates = {
#             "x": "-",
#             "y": "-",
#             "z": "-",
#             "timestamp": datetime.now().isoformat()
#         }
#         print("Canvas Reset Signal Sent")
#         return coordinates
    
#     # Normal coordinate generation
#     # Center point of the circle
#     center_lat = 45.3876
#     center_lon = -75.6960
    
#     # Radius of the circle (in degrees)
#     radius = 0.001
    
#     # Calculate angle based on current time
#     angle = (time.time() % (2 * math.pi))
    
#     # Calculate new position
#     current_lat = center_lat + radius * math.cos(angle)
#     current_lon = center_lon + radius * math.sin(angle)

#     # Randomly decide to set z > 0 (approximately 20% of the time)
#     z_value = random.uniform(1, 5) if random.random() < 0.2 else 0

#     coordinates = {
#         "x": current_lat,
#         "y": current_lon,
#         "z": z_value,
#         "timestamp": datetime.now().isoformat()
#     }
    
#     # Print whether this point will be visible in the plot
#     if z_value == 0:
#         print("Point will be visible (z=0)")
#     else:
#         print(f"Point will be invisible (z={z_value:.2f})")
    
#     return coordinates

# def main():
#     client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
#     client.on_connect = on_connect
    
#     # Set credentials
#     client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    
#     # Enable SSL/TLS
#     client.tls_set()
    
#     # Connect to Solace Cloud
#     client.connect(MQTT_HOST, MQTT_PORT, 60)
    
#     # Start the MQTT client loop in the background
#     client.loop_start()
    
#     try:
#         while True:
#             bus_data = simulate_circular_movement()
#             topic = "coordinates"
#             client.publish(topic, json.dumps(bus_data), qos=1, retain=False)
#             print(f"Published: {bus_data}")
#             print(f"Time until next reset: {RESET_INTERVAL - (time.time() - last_reset_time):.1f} seconds")
#             print("-------------------")
#             time.sleep(0.1)  # Smaller sleep time for smoother movement
            
#     except KeyboardInterrupt:
#         client.loop_stop()
#         client.disconnect()

# if __name__ == "__main__":
#     main()
# # import paho.mqtt.client as mqtt
# # import json
# # import time
# # import math
# # import random
# # from datetime import datetime
# # import configparser

# # # Load configuration
# # def load_config():
# #     config = configparser.ConfigParser()
# #     config.read('config.properties')
# #     return {
# #         'host': config.get('mqtt', 'host'),
# #         'port': config.getint('mqtt', 'port'),
# #         'username': config.get('mqtt', 'username'),
# #         'password': config.get('mqtt', 'password'),
# #     }

# # config = load_config()

# # # Use configuration values
# # MQTT_HOST = config['host']
# # MQTT_PORT = config['port']
# # MQTT_USER = config['username']
# # MQTT_PASSWORD = config['password']

# # def on_connect(client, userdata, flags, reason_code, properties=None):
# #     print(f"Connected with result code {reason_code}")

# # def simulate_circular_movement():
# #     # Center point of the circle
# #     center_lat = 45.3876
# #     center_lon = -75.6960
    
# #     # Radius of the circle (in degrees)
# #     radius = 0.001
    
# #     # Calculate angle based on current time
# #     angle = (time.time() % (2 * math.pi))
    
# #     # Calculate new position
# #     current_lat = center_lat + radius * math.cos(angle)
# #     current_lon = center_lon + radius * math.sin(angle)

# #     # Randomly decide to set z > 0 (approximately 20% of the time)
# #     z_value = random.uniform(1, 5) if random.random() < 0.2 else 0

# #     coordinates = {
# #         "x": current_lat,
# #         "y": current_lon,
# #         "z": z_value,
# #         "timestamp": datetime.now().isoformat()
# #     }
    
# #     # Print whether this point will be visible in the plot
# #     if z_value == 0:
# #         print("Point will be visible (z=0)")
# #     else:
# #         print(f"Point will be invisible (z={z_value:.2f})")
    
# #     return coordinates

# # def main():
# #     client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# #     client.on_connect = on_connect
    
# #     # Set credentials
# #     client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    
# #     # Enable SSL/TLS
# #     client.tls_set()
    
# #     # Connect to Solace Cloud
# #     client.connect(MQTT_HOST, MQTT_PORT, 60)
    
# #     # Start the MQTT client loop in the background
# #     client.loop_start()
    
# #     try:
# #         while True:
# #             bus_data = simulate_circular_movement()
# #             topic = "coordinates"
# #             client.publish(topic, json.dumps(bus_data))
# #             print(f"Published: {bus_data}")
# #             print("-------------------")
# #             time.sleep(0.1)  # Smaller sleep time for smoother movement
            
# #     except KeyboardInterrupt:
# #         client.loop_stop()
# #         client.disconnect()

# # if __name__ == "__main__":
# #     main()
