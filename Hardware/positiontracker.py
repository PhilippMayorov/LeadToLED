import serial  # For serial communication
import matplotlib.pyplot as plt  # For plotting
from matplotlib.animation import FuncAnimation  # For real-time plot updates

# Configuration
serial_port = "COM3"  # Replace with your port, e.g., "COM3" for Windows or "/dev/ttyUSB0" for Linux/Mac
baud_rate = 9600  # Must match the baud rate in the Arduino code

# Open serial connection
try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    print(f"Connected to {serial_port} at {baud_rate} baud.")
except Exception as e:
    print(f"Error: Could not connect to {serial_port}.")
    print(e)
    exit()

# Data storage for plotting
x_data, y_data, z_data = [], [], []

# Plotting function
def update(frame):
    global x_data, y_data, z_data

    # Read a line of data from the serial port
    line = ser.readline().decode('utf-8').strip()  # Decode and clean up the data
    if line:  # If valid data is received
        try:
            # Parse the CSV data
            ax, ay, az = map(int, line.split(','))
            print(f"Accel X: {ax}, Accel Y: {ay}, Accel Z: {az}")  # Debugging output

            # Append to the data lists
            x_data.append(ax)
            y_data.append(ay)
            z_data.append(az)

            # Limit the data to the last 100 points for better visualization
            if len(x_data) > 100:
                x_data.pop(0)
                y_data.pop(0)
                z_data.pop(0)

            # Clear the plot and update it
            plt.cla()
            plt.plot(x_data, label="Accel X", color="red")
            plt.plot(y_data, label="Accel Y", color="green")
            plt.plot(z_data, label="Accel Z", color="blue")
            plt.legend(loc="upper right")
            plt.title("Real-Time Accelerometer Data")
            plt.xlabel("Time (arbitrary units)")
            plt.ylabel("Acceleration")
            plt.grid(True)
        except ValueError:
            print("Invalid data received, skipping...")  # Handle parsing errors gracefully

# Set up the plot
fig = plt.figure()
ani = FuncAnimation(fig, update, interval=100)  # Update every 100 ms

# Show the plot
try:
    plt.show()
except KeyboardInterrupt:
    print("Exiting plot...")

# Clean up
ser.close()

