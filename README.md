# OC Transpo Real-Time Bus Tracking System

A demonstration project showing how to use Solace Cloud for real-time event streaming of bus locations using MQTT.

## Overview

This project simulates a real-time bus tracking system similar to what OC Transpo might use to track their fleet. It consists of two main components:

1. A bus simulator that generates and publishes location data
2. A tracking server that receives and displays updates from all buses

## Prerequisites

- Python 3.7 or higher
- A free Solace Cloud account
- Basic understanding of Python programming

## Setting Up Your Environment

### 1. Create a Solace Cloud Account

1. Visit [console.solace.cloud](https://console.solace.cloud)
2. Sign up for a free account
3. Register your team on [uottahack.solace.cloud](https://uottahack.solace.cloud/)
4. Create a new messaging service:
   - Click "Create Messaging Service"
   - Choose "Free Plan"
   - Name it "bus-tracking-service"
   - Select your preferred region
   - Click "Create"

### 2. Get Your Connection Details

1. In your Solace Cloud Console, click on your messaging service
2. Click "Connect"
3. Select "MQTT"
4. Note down the following details:
   - MQTT Host URL
   - Port (8883 for secured connection)
   - Message VPN
   - Client Username
   - Client Password

### 3. Set Up Python Environment

```bash
# Cloning Repository
git clone https://github.com/mo-radwan1/solace-octranspo-tracker

cd bus-tracking

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

> Note: The project uses the following Python packages:
>
> - `paho-mqtt`: For MQTT communication (needs to be installed)
> - `json`: Built-in Python module
> - `datetime`: Built-in Python module
> - `configparser`: Built-in Python module
> - `random`: Built-in Python module
> - `time`: Built-in Python module

## Project Structure

```
bus-tracking/
│
├── bus_simulator.py
├── tracking_server.py
└── README.md
```

## Implementation Details

### Bus Simulator (`bus_simulator.py`)

This script simulates a bus moving along a route:

- ✨ Generates random movement patterns
- 📦 Creates JSON messages with bus location data
- 🔄 Publishes updates every 2 seconds
- 🔒 Uses secure MQTT connection to Solace Cloud

### Tracking Server (`tracking_server.py`)

This script receives and displays bus updates:

- 📡 Subscribes to all bus location topics
- 🔄 Processes incoming JSON messages
- 📊 Displays formatted location updates
- 🔌 Maintains persistent connection to Solace Cloud

## Message Format

Bus location updates use the following JSON structure:

```json
{
  "bus_id": "Bus-001",
  "route": "Route-95",
  "latitude": 45.3876,
  "longitude": -75.696,
  "timestamp": "2023-11-09T14:30:00",
  "speed": 45.5
}
```

## Topic Structure

```
Topic format: oc-transpo/bus/{bus_id}/location
Example: oc-transpo/bus/Bus-001/location
```

## Configurations

### Setting up the Configuration File

1. Copy the template file to create your configuration:

   ```bash
   cp config.properties.template config.properties
   ```

2. Edit `config.properties` with your Solace Cloud credentials:

   ```properties
   [mqtt]
   host=YOUR_MQTT_HOST        # From Solace Cloud Console
   port=8883                  # Default secure MQTT port
   username=YOUR_USERNAME     # From Solace Cloud Console
   password=YOUR_PASSWORD     # From Solace Cloud Console

   [bus]
   id=Bus-001                 # Can be customized
   route=Route-95            # Can be customized
   update_interval=2         # Update frequency in seconds
   ```

3. Verify your configuration:
   - Ensure the file is named exactly `config.properties`
   - Double-check your credentials from the Solace Cloud Console
   - Make sure there are no extra spaces around the `=` signs

> ⚠️ Important: Never commit your `config.properties` file with real credentials to version control.
> The `.gitignore` file should include `config.properties` but allow `config.properties.template`.

Update your Solace credentials in both Python files:

```python
MQTT_HOST = "YOUR_MQTT_HOST"
MQTT_PORT = 8883
MQTT_USER = "YOUR_USERNAME"
MQTT_PASSWORD = "YOUR_PASSWORD"
```

## Running the Application

1. **Start the Tracking Server:**

   ```bash
   python tracking_server.py
   ```

2. **Start the Bus Simulator:**
   ```bash
   python bus_simulator.py
   ```

### Expected Output

```
Connected with result code 0
Received update from Bus-001:
Location: (45.3876, -75.6960)
Speed: 45.5 km/h
Timestamp: 2023-11-09T14:30:00
-------------------
```

## Troubleshooting

### Common Issues

1. **Connection Failed**

   - ✔️ Verify credentials
   - ✔️ Check internet connection
   - ✔️ Confirm Solace service status

2. **Import Errors**

   - ✔️ Verify package installation
   - ✔️ Check virtual environment activation

3. **SSL/TLS Errors**
   - ✔️ Confirm port 8883 usage
   - ✔️ Verify SSL library installation

## Extending the Project

### Suggested Enhancements

1. **Multiple Buses**

   - Add multiple simulator instances
   - Implement different routes

2. **New Features**

   - Passenger counting
   - Status tracking
   - Route adherence monitoring

3. **Visualization**
   - Web interface
   - Map integration
   - Historical data views

## Resources

- [Solace Documentation](https://docs.solace.com)
- [MQTT Protocol Documentation](https://mqtt.org/documentation)
- [Paho MQTT Python Client](https://www.eclipse.org/paho/clients/python)

---

🚀 Happy coding! This project demonstrates event-driven architecture and real-time data streaming using Solace Cloud.
