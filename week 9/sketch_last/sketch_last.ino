#include <DHT.h>

#define DHTPIN   2        
#define DHTTYPE  DHT22    

DHT dht(DHTPIN, DHTTYPE);

bool readDHT(float &tC, float &h) {
  
  for (int i = 0; i < 3; i++) {
    h  = dht.readHumidity();
    tC = dht.readTemperature();  // reads temp in C
    if (!isnan(h) && !isnan(tC)) return true;
    delay(2100);               
  }
  return false;
}

void setup() {
  Serial.begin(9600);
  while (!Serial) {}             
  pinMode(DHTPIN, INPUT_PULLUP); 
  dht.begin();

  delay(3000);                 
  Serial.println("Temperature_C,Humidity_%");
}

void loop() {
  float tC, h;
  if (readDHT(tC, h)) {
    Serial.print(tC, 1);
    Serial.print(',');
    Serial.println(h, 1);
  } else {
    Serial.println("nan,nan");  
  }
  delay(60000);                 
}