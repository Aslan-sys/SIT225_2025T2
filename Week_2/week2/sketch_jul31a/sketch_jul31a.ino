// inclduing the dht libary
#include <DHT.h>
#define DHTPIN 2  // showcaseing what digital pin number in this case 2
#define DHTTYPE DHT22  // defining the 22 dht sensor
DHT dht(DHTPIN, DHTTYPE);

// variables to store our data humidity and temperture
float hum, temp;

void setup() {
  // Set baud rate for serial communication which matches pythons
  Serial.begin(9600);

  // initialises libarary
  dht.begin();
}

void loop() {
  // reading the data
  hum = dht.readHumidity();
  temp = dht.readTemperature();

  // Print data to serial port - a compact way
  Serial.println(String(hum) + "," + String(temp));
  
  // wait a while
  delay(15*1000);
}