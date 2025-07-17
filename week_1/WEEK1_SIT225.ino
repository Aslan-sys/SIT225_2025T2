void setup() {
  pinMode(LED_BUILTIN, OUTPUT); // calibirated the LED as an output
  Serial.begin(9600); // serial communication at 9600 baud
  randomSeed(analogRead(0)); // Seed random number generator
}

void loop() {
  // Check if data is available on serial port
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n'); // Read until newline
    int blinkCount = input.toInt(); // Convert string to integer

    // Validate blink count
    if (blinkCount > 0) {
      // LED will blink for the specified number of times
      for (int i = 0; i < blinkCount; i++) {
        digitalWrite(LED_BUILTIN, HIGH); // Turns LED on
        delay(500); // On for 0.5 seconds
        digitalWrite(LED_BUILTIN, LOW); // Turns LED off
        delay(500); // Off for 0.5 seconds 
      }

      // Generates a random number (1-5) for Python to sleep / freeze
      int delayRandom = random(1, 6); // random(1, 6) generates 1 to 5
      Serial.println(delayRandom); // Send number with newline
      Serial.flush(); // Ensure data is sent before proceeding
    }
  }
}