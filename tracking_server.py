import paho.mqtt.client as mqtt
import json
import configparser

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

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected with result code {reason_code}")
    # Subscribe to all bus location updates
    client.subscribe("oc-transpo/bus/+/location")

def on_message(client, userdata, message):
    try:
        # Parse the JSON message
        bus_data = json.loads(message.payload.decode())
        print(f"Received update from {bus_data['bus_id']}:")
        print(f"Location: ({bus_data['latitude']}, {bus_data['longitude']})")
        print(f"Speed: {bus_data['speed']} km/h")
        print(f"Timestamp: {bus_data['timestamp']}")
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
    
    try:
        # Process messages forever
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nDisconnecting from broker...")
        client.loop_stop()
        client.disconnect()
        print("Disconnected successfully")

if __name__ == "__main__":
    main()