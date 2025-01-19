//#include "Wire.h" // (Uncomment this you should have wire.h in your ardunio ide) Include the Wire library for I2C communication

const int MPU_ADDR = 0x68; // I2C address of the MPU-6050. If AD0 is HIGH, the address will be 0x69.

int16_t accelerometer_x, accelerometer_y, accelerometer_z; // Variables for accelerometer raw data
int16_t gyro_x, gyro_y, gyro_z;                           // Variables for gyro raw data
int16_t temperature;                                      // Variable for temperature data

void setup() {
  Serial.begin(9600);          // Initialize serial communication at 9600 baud
  Wire.begin();                // Initialize I2C communication
  Wire.beginTransmission(MPU_ADDR); // Start communication with the MPU-6050
  Wire.write(0x6B);                 // Access the PWR_MGMT_1 register
  Wire.write(0);                    // Set the register to 0 to wake up the MPU-6050
  Wire.endTransmission(true);       // End the transmission
}

void loop() {
  // Request accelerometer, temperature, and gyro data
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);                // Starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);     // End transmission but keep the I2C bus active
  Wire.requestFrom(MPU_ADDR, 7 * 2, true); // Request 14 bytes (7 registers, 2 bytes each)

  // Read accelerometer data
  accelerometer_x = Wire.read() << 8 | Wire.read(); // Read ACCEL_XOUT_H and ACCEL_XOUT_L
  accelerometer_y = Wire.read() << 8 | Wire.read(); // Read ACCEL_YOUT_H and ACCEL_YOUT_L
  accelerometer_z = Wire.read() << 8 | Wire.read(); // Read ACCEL_ZOUT_H and ACCEL_ZOUT_L

  // Skip temperature and gyro data if you only need accelerometer data for Python parsing
//  Wire.read(); Wire.read(); // TEMP_OUT_H and TEMP_OUT_L
  Wire.read(); Wire.read(); // GYRO_XOUT_H and GYRO_XOUT_L
  Wire.read(); Wire.read(); // GYRO_YOUT_H and GYRO_YOUT_L
  Wire.read(); Wire.read(); // GYRO_ZOUT_H and GYRO_ZOUT_L

  // Send accelerometer data in CSV format: "aX,aY,aZ"
  Serial.print(accelerometer_x);
  Serial.print(",");
  Serial.print(accelerometer_y);
  Serial.print(",");
  Serial.println(accelerometer_z); // Print the last value with a newline

  delay(100); // Delay for 100ms (adjust if needed for your application)
}