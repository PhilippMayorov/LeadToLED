import paho.mqtt.client as mqtt
import json
import time
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
        'bus_id': config.get('bus', 'id'),
        'route': config.get('bus', 'route'),
        'update_interval': config.getint('bus', 'update_interval')
    }

config = load_config()

# Use configuration values
MQTT_HOST = config['host']
MQTT_PORT = config['port']
MQTT_USER = config['username']
MQTT_PASSWORD = config['password']
BUS_ID = config['bus_id']
ROUTE = config['route']
UPDATE_INTERVAL = config['update_interval']

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected with result code {reason_code}")

def simulate_bus_movement():
    # Simulating movement along baseline station to orleans
    base_lat = 45.3876
    base_lon = -75.6960
    
    # Simulate movement by adding small random changes
    current_lat = base_lat + random.uniform(-0.001, 0.001)
    current_lon = base_lon + random.uniform(-0.001, 0.001)
    
    bus_data = {
        "bus_id": BUS_ID,
        "route": ROUTE,
        "latitude": current_lat,
        "longitude": current_lon,
        "timestamp": datetime.now().isoformat(),
        "speed": random.uniform(30, 50)  # km/h
    }
    
    return bus_data

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
            bus_data = simulate_bus_movement()
            # Publish to topic: oc-transpo/bus/{bus_id}/location
            topic = f"oc-transpo/bus/{BUS_ID}/location"
            client.publish(topic, json.dumps(bus_data))
            print(f"Published: {bus_data}")
            time.sleep(UPDATE_INTERVAL)  # Update every update_interval seconds
            
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()