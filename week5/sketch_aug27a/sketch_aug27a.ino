#include <Arduino_LSM6DS3.h> // libaries

float gx, gy, gz; //  the variables of our data

void setup() {
  Serial.begin(9600);  // baud rate
  while (!Serial);     // waits for port
  Serial.println("Started"); // displays text 

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.println(
    "Gyroscope sample rate = " 
    + String(IMU.gyroscopeSampleRate()) + " Hz");
}

void loop() {
  // reads abd checks the  gyroscope data 
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(gx, gy, gz);
  }
  
  Serial.println(
    String(gx, 3) + ", " + String(gy, 3) + ", " + String(gz, 3)); // sends the data to the serial port
  
  delay(50); // 20hz
}