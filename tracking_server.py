import paho.mqtt.client as mqtt
import json
import configparser
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import numpy as np

# Create deques to store coordinate history
x_coords = deque(maxlen=100)  # Stores last 100 points
y_coords = deque(maxlen=100)
z_coords = deque(maxlen=100)

def load_config():
    config = configparser.ConfigParser()
    config.read('config.properties')
    return {
        'host': config.get('mqtt', 'host'),
        'port': config.getint('mqtt', 'port'),
        'username': config.get('mqtt', 'username'),
        'password': config.get('mqtt', 'password')
    }

# Load configuration
config = load_config()

# Use configuration values
MQTT_HOST = config['host']
MQTT_PORT = config['port']
MQTT_USER = config['username']
MQTT_PASSWORD = config['password']

# Set up the figure and subplot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111)
lines = []  # Store multiple line objects

# Initialize the plot
def init():
    ax.set_title('Real-time Coordinate Tracking (Z=0 only)')
    ax.set_xlabel('Y Coordinate (Longitude)')
    ax.set_ylabel('X Coordinate (Latitude)')
    ax.grid(True)
    return []

# Animation update function
def update(frame):
    global lines
    
    # Clear previous lines
    for line in lines:
        line.remove()
    lines.clear()
    
    if len(x_coords) > 0:
        # Create segments of continuous z=0 points
        segments_x = []
        segments_y = []
        current_segment_x = []
        current_segment_y = []
        
        # Group continuous z=0 points into segments
        for x, y, z in zip(x_coords, y_coords, z_coords):
            if z == 0:
                current_segment_x.append(x)
                current_segment_y.append(y)
            else:
                if current_segment_x:  # If we have points in the current segment
                    segments_x.append(current_segment_x)
                    segments_y.append(current_segment_y)
                    current_segment_x = []
                    current_segment_y = []
        
        # Add the last segment if it exists
        if current_segment_x:
            segments_x.append(current_segment_x)
            segments_y.append(current_segment_y)
        
        # Plot each segment as a separate line
        for seg_x, seg_y in zip(segments_x, segments_y):
            line, = ax.plot(seg_y, seg_x, 'b-')
            lines.append(line)
            
            # Add point at the end of each segment
            point, = ax.plot([seg_y[-1]], [seg_x[-1]], 'ro')
            lines.append(point)
        
        # Adjust plot limits dynamically
        ax.relim()
        ax.autoscale_view()
    
    return lines

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected with result code {reason_code}")
    client.subscribe("coordinates")

def on_message(client, userdata, message):
    try:
        # Parse the JSON message
        coordinates = json.loads(message.payload.decode())
        print(f"Received coordinates:")
        print(f"Location: ({coordinates['x']}, {coordinates['y']}, {coordinates['z']})")
        
        # Add new coordinates to deques
        x_coords.append(coordinates['x'])
        y_coords.append(coordinates['y'])
        z_coords.append(coordinates['z'])

        # Print whether point will be plotted
        if coordinates['z'] == 0:
            print("Point will be plotted (z=0)")
        else:
            print("Point will be skipped (z≠0)")

        print("-------------------")
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    
    # Set credentials
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    
    # Enable SSL/TLS
    client.tls_set()
    
    # Connect to Solace Cloud
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    
    # Start MQTT client in a non-blocking way
    client.loop_start()
    
    # Set up animation
    ani = FuncAnimation(fig, update, init_func=init, interval=100, blit=True)
    
    try:
        # Show the plot
        plt.show()
        
    except KeyboardInterrupt:
        print("\nDisconnecting from broker...")
        client.loop_stop()
        client.disconnect()
        print("Disconnected successfully")

if __name__ == "__main__":
    main()
    
# import paho.mqtt.client as mqtt
# import json
# import configparser
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# from collections import deque
# import numpy as np

# # Create deques to store coordinate history
# x_coords = deque(maxlen=100)  # Stores last 100 points
# y_coords = deque(maxlen=100)
# z_coords = deque(maxlen=100)

# def load_config():
#     config = configparser.ConfigParser()
#     config.read('config.properties')
#     return {
#         'host': config.get('mqtt', 'host'),
#         'port': config.getint('mqtt', 'port'),
#         'username': config.get('mqtt', 'username'),
#         'password': config.get('mqtt', 'password')
#     }

# # Load configuration
# config = load_config()

# # Use configuration values
# MQTT_HOST = config['host']
# MQTT_PORT = config['port']
# MQTT_USER = config['username']
# MQTT_PASSWORD = config['password']

# # Set up the figure and subplot
# fig = plt.figure(figsize=(10, 8))
# ax = fig.add_subplot(111)
# line, = ax.plot([], [], 'b-', label='Movement Path')
# point, = ax.plot([], [], 'ro', label='Current Position')

# # Initialize the plot
# def init():
#     ax.set_title('Real-time Coordinate Tracking')
#     ax.set_xlabel('Y Coordinate (Longitude)')
#     ax.set_ylabel('X Coordinate (Latitude)')
#     ax.grid(True)
#     ax.legend()
#     return line, point

# # Animation update function
# def update(frame):
#     if len(x_coords) > 0:
#         line.set_data(list(y_coords), list(x_coords))
#         point.set_data([y_coords[-1]], [x_coords[-1]])
        
#         # Adjust plot limits dynamically
#         ax.relim()
#         ax.autoscale_view()
#     return line, point

# def on_connect(client, userdata, flags, reason_code, properties=None):
#     print(f"Connected with result code {reason_code}")
#     client.subscribe("coordinates")

# def on_message(client, userdata, message):
#     try:
#         # Parse the JSON message
#         coordinates = json.loads(message.payload.decode())
#         print(f"Received coordinates:")
#         print(f"Location: ({coordinates['x']}, {coordinates['y']}, {coordinates['z']})")
        
#         # Add new coordinates to deques
#         x_coords.append(coordinates['x'])
#         y_coords.append(coordinates['y'])
#         z_coords.append(coordinates['z'])

#         print("-------------------")
#     except Exception as e:
#         print(f"Error processing message: {e}")

# def main():
#     client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
#     client.on_connect = on_connect
#     client.on_message = on_message
    
#     # Set credentials
#     client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    
#     # Enable SSL/TLS
#     client.tls_set()
    
#     # Connect to Solace Cloud
#     client.connect(MQTT_HOST, MQTT_PORT, 60)
    
#     # Start MQTT client in a non-blocking way
#     client.loop_start()
    
#     # Set up animation
#     ani = FuncAnimation(fig, update, init_func=init, interval=100, blit=True)
    
#     try:
#         # Show the plot
#         plt.show()
        
#     except KeyboardInterrupt:
#         print("\nDisconnecting from broker...")
#         client.loop_stop()
#         client.disconnect()
#         print("Disconnected successfully")

# if __name__ == "__main__":
#     main()