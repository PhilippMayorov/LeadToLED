import paho.mqtt.client as mqtt
import json
import time
import math
import random
from datetime import datetime
import configparser

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
RESET_INTERVAL = random.uniform(2, 6)  # Random interval between 5 and 15 seconds

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

def simulate_circular_movement():
    global last_reset_time
    
    # Check if it's time to reset
    if should_reset():
        coordinates = {
            "x": "-",
            "y": "-",
            "z": "-",
            "timestamp": datetime.now().isoformat()
        }
        print("Canvas Reset Signal Sent")
        return coordinates
    
    # Normal coordinate generation
    # Center point of the circle
    center_lat = 45.3876
    center_lon = -75.6960
    
    # Radius of the circle (in degrees)
    radius = 0.001
    
    # Calculate angle based on current time
    angle = (time.time() % (2 * math.pi))
    
    # Calculate new position
    current_lat = center_lat + radius * math.cos(angle)
    current_lon = center_lon + radius * math.sin(angle)

    # Randomly decide to set z > 0 (approximately 20% of the time)
    z_value = random.uniform(1, 5) if random.random() < 0.2 else 0

    coordinates = {
        "x": current_lat,
        "y": current_lon,
        "z": z_value,
        "timestamp": datetime.now().isoformat()
    }
    
    # Print whether this point will be visible in the plot
    if z_value == 0:
        print("Point will be visible (z=0)")
    else:
        print(f"Point will be invisible (z={z_value:.2f})")
    
    return coordinates

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
            bus_data = simulate_circular_movement()
            topic = "coordinates"
            client.publish(topic, json.dumps(bus_data))
            print(f"Published: {bus_data}")
            print(f"Time until next reset: {RESET_INTERVAL - (time.time() - last_reset_time):.1f} seconds")
            print("-------------------")
            time.sleep(0.1)  # Smaller sleep time for smoother movement
            
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

# def on_connect(client, userdata, flags, reason_code, properties=None):
#     print(f"Connected with result code {reason_code}")

# def simulate_circular_movement():
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
#             client.publish(topic, json.dumps(bus_data))
#             print(f"Published: {bus_data}")
#             print("-------------------")
#             time.sleep(0.1)  # Smaller sleep time for smoother movement
            
#     except KeyboardInterrupt:
#         client.loop_stop()
#         client.disconnect()

# if __name__ == "__main__":
#     main()
