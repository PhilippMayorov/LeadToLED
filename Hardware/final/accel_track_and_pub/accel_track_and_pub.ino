#include <WiFi.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>
#include "Wire.h"
#include "credentials.h"

// MPU-6050 settings
const int MPU_ADDR = 0x68;
int16_t accelerometer_x, accelerometer_y, accelerometer_z;

// Create a secure WiFi client
WiFiClientSecure espClient;
PubSubClient client(espClient);

unsigned long lastMillis = 0;

void setup_wifi() {
  delay(10);
  Serial.println("Connecting to WiFi...");
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  // Handle incoming messages if needed
}

void reconnect() {
  while (!client.connected()) {
    Serial.println("Attempting MQTT connection...");
    
    if (client.connect(client_id, mqtt_username, mqtt_password)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  
  // Setup WiFi and MQTT
  setup_wifi();
  espClient.setInsecure();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);

  // Setup MPU-6050
  Wire.begin();
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
}

void readAccelerometer() {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 7 * 2, true);

  accelerometer_x = Wire.read() << 8 | Wire.read();
  accelerometer_y = Wire.read() << 8 | Wire.read();
  accelerometer_z = Wire.read() << 8 | Wire.read();

  // Skip temperature and gyro data
  for(int i = 0; i < 8; i++) {
    Wire.read();
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Publish every 100ms
  if (millis() - lastMillis > 100) {
    // Read accelerometer data
    readAccelerometer();
    
    // Create JSON string with accelerometer data
    String jsonString = "{\"x\":" + String(accelerometer_x) + 
                       ",\"y\":" + String(accelerometer_y) + 
                       ",\"z\":" + String(accelerometer_z) + "}";
    
    // Publish the data
    if (client.publish(topic, jsonString.c_str())) {
      Serial.println("Published: " + jsonString);
    } else {
      Serial.println("Failed to publish message");
    }
    
    lastMillis = millis();
  }
}