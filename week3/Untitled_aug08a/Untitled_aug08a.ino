#include "arduino_secrets.h"
#include "thingProperties.h"
#include <math.h>

const int TRIG_PIN  = 9;
const int ECHO_PIN  = 10;

// --- Sampling & detection params ---
const unsigned long PERIOD_MS        = 1000;   // ~1 Hz
const float         MOVEMENT_DELTA_CM = 3.0;   // change threshold to flag "moving"

// --- State ---
float lastDistance = NAN;          
unsigned long lastSample = 0;

// Forward declaration
float measureDistanceCm();

void setup() {
  // Local hardware init
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  Serial.begin(115200);
  delay(1000);
  Serial.println("timestamp,distance_cm,moving");

  // === Arduino Cloud init ===
  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);

  // Optional: verbose connection logs
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
}

void loop() {
  // Keep the IoT connection alive and handle variable sync
  ArduinoCloud.update();

  // Periodic sample
  unsigned long now = millis();
  if (now - lastSample < PERIOD_MS) return;
  lastSample = now;

  // Measure RAW distance
  float d = measureDistanceCm();
  if (isnan(d)) {
    // skip invalid reads (timeout/out-of-range)
    return;
  }

  // Simple movement detection using RAW values
  bool isMoving = false;
  if (!isnan(lastDistance)) {
    isMoving = (fabsf(d - lastDistance) > MOVEMENT_DELTA_CM);
  }

  // === Update Cloud variables with RAW distance ===
  // Ensure your Thing defines: distance_cm (FLOAT RO), moving (BOOL RO)
  distance_cm = d;
  moving      = isMoving;

  // Also print CSV locally (handy for Python logging)
  unsigned long secs = now / 1000;
  Serial.print(secs); Serial.print(",");
  Serial.print(d, 1); Serial.print(",");
  Serial.println(isMoving ? 1 : 0);

  // Store RAW distance for next comparison
  lastDistance = d;
}

// --- HC-SR04 measurement helper ---
float measureDistanceCm() {
  // Trigger pulse
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(3);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Measure echo with a timeout (~30 ms)
  unsigned long duration = pulseIn(ECHO_PIN, HIGH, 30000UL);
  if (duration == 0) return NAN; // timeout -> invalid

  // Convert time-of-flight to distance (cm)
  float distance = (duration * 0.0343f) / 2.0f;

  // Clip to sensor's reasonable range
  if (distance < 1 || distance > 450) return NAN;
  return distance;
}

void onRandomTemperatureChange()  {
  // (unused in this sketch)
}