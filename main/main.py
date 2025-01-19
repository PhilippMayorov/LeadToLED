from mqtt_handler import MQTTHandler
from mongodb_handler import MongoDBHandler
from plotter import Plotter

def main():
    try:
        # Initialize components
        mongo_handler = MongoDBHandler()
        plotter = Plotter()
        mqtt_handler = MQTTHandler(mongo_handler=mongo_handler, plotter=plotter)

        # Test MongoDB connection
        if not mongo_handler.test_connection():
            print("Failed to connect to MongoDB. Exiting...")
            return

        # Connect to MQTT broker
        if not mqtt_handler.connect():
            print("Failed to connect to MQTT broker. Exiting...")
            return

        # Start MQTT client
        mqtt_handler.start()

        # Show the plot (this will block until the window is closed)
        plotter.start_animation()

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        # Clean up
        mqtt_handler.stop()
        mongo_handler.close_connection()
        print("Disconnected successfully")

if __name__ == "__main__":
    main() 