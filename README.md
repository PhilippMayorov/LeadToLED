# LeadToLED: Digital Pen Motion Tracking System 🖊️✨

LeadToLED is an innovative system that captures physical writing movements and converts them into digital data using accelerometer and gyroscope sensors. The project combines hardware and software components to track pen movements in real-time and visualize them digitally.

## Features 🌟

- Real-time motion tracking using MPU-6050 accelerometer/gyroscope
- MQTT-based data transmission over secure connection
- MongoDB integration for storing writing sessions
- Live visualization of pen movements
- Multi-canvas support within sessions
- Automatic calibration system **[SOON]**
- Position tracking with drift compensation
- Coordinate logging system

> **Note**: Hardware inconsistency can make things tricky! We've had to adopt some creative (but unfortunately somewhat restraining) solutions to sketching in order to ensure accuracy and usability.

## Prerequisites 📋

- Python 3.7+
- Arduino IDE (for hardware component)
- MongoDB Account
- Solace MQTT Broker Account
- Required Hardware:
    - ESP32 or compatible microcontroller
    - MPU-6050 sensor module

## Installation 🔧

1. Clone the repository:

```bash
git clone https://github.com/yourusername/leadtoLED.git
cd leadtoLED
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your environment:
      - Copy `config.properties.template` to `config.properties`
      - Fill in your MQTT and MongoDB credentials
      - Create a `.env` file with your MongoDB URI

4. Set up the hardware:
      - Copy `credentials.h.example.h` to `credentials.h`
      - Update with your WiFi and MQTT credentials
      - Flash the Arduino code to your ESP32

## Project Structure 📁

```
leadtoLED/
├── Hardware/
│   ├── final/
│   │   └── accel_track_and_pub/    # ESP32 accelerometer code
│   └── positiontracker.py          # Position tracking utilities
├── main/
│   ├── backend/
│   │   ├── getCoords.py           # Coordinate retrieval
│   │   ├── mongodb_handler.py     # MongoDB operations
│   │   └── seedDB.py             # Database initialization
│   ├── frontend/
│   │   ├── Canvas.py             # Main visualization
│   │   └── plotter.py           # Real-time plotting
│   └── mqtt_handler.py           # MQTT communication
├── config.properties.template     # Configuration template
└── requirements.txt              # Python dependencies
```

## Usage 🚀

1. Start the MongoDB connection:

```bash
python main/backend/seedDB.py
```

2. Launch the visualization canvas:

```bash
python main/Canvas.py
```

3. Power up the hardware device and start writing!

## How It Works 🔍

1. The MPU-6050 sensor captures acceleration and gyroscope data
2. Data is transmitted via MQTT to the server
3. The motion processor converts raw sensor data into position coordinates
4. Real-time visualization shows the writing path
5. Data is stored in MongoDB for later retrieval

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- MPU-6050 community for sensor documentation
- Solace for MQTT broker services
- MongoDB Atlas for database hosting
