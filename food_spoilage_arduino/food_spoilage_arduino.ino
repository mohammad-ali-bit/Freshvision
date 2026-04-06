/*
  FreshVision Arduino - Hardware Spoilage Detector 
  -----------------------------------------------
  Author: AI Engineer
  Date: 2026-04-01
  
  Description:
  This script uses an MQ Gas Sensor (MQ-2 by default) to detect the 
  gasses emitted by rotting food (methane, alcohol, etc). 
  If the concentration crosses a threshold, it triggers a RED LED and a Piezo Buzzer.
  Otherwise, it keeps a GREEN LED illuminated to indicate freshness.
  
  Hardware Pinout:
  - MQ-2 Analog Pin (A0) -> Arduino A0
  - Green LED (Fresh)    -> Arduino Digital Pin 8 (with 220 ohm resistor)
  - Red LED (Spoiled)    -> Arduino Digital Pin 9 (with 220 ohm resistor)
  - Piezo Buzzer (+ pin) -> Arduino Digital Pin 10
  - GND / 5V             -> Connect sensor and LEDs to Ground and 5V respectively.
  
  Note on Upgrades:
  While the MQ-2 detects general combustible gasses and smoke, it can be seamlessly 
  swapped for an MQ-135 (Air Quality / Ammonia) or MQ-3 (Alcohol/Ethanol) for 
  higher precision without changing any code. Just swap the sensor and adjust the threshold!
*/

// --- Pin Definitions ---
const int MQ_SENSOR_PIN = A0;   // Analog input pin from the sensor
const int GREEN_LED_PIN = 8;    // Digital output pin for Fresh state
const int RED_LED_PIN = 9;      // Digital output pin for Spoiled state
const int BUZZER_PIN = 10;      // Digital output pin for audible alarm

// --- Calibration Threshold ---
// This value determines the point at which food is considered "spoiling".
// The MQ sensor returns an analog value from 0 to 1023.
// You will need to monitor the Serial Monitor and adjust this value 
// based on what your sensor outputs near fresh vs. rotting food!
int SPOILAGE_THRESHOLD = 400;   

void setup() {
  // Initialize Serial Monitor for debugging and calibration
  Serial.begin(9600);
  
  // Initialize digital pins as outputs
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(MQ_SENSOR_PIN, INPUT);

  // Initial feedback sound (startup chirp)
  Serial.println("System Initializing: Warming up MQ Sensor...");
  tone(BUZZER_PIN, 1000, 200); // 1000Hz for 200ms
  delay(300);
  tone(BUZZER_PIN, 1500, 200); 
  delay(2000); // Give the sensor a moment to warm up
}

void loop() {
  // 1. Read the gas concentration value from the MQ-2 sensor
  int gasLevel = analogRead(MQ_SENSOR_PIN);
  
  // 2. Print the value to the Serial Monitor for calibration
  Serial.print("Current Gas Level: ");
  Serial.print(gasLevel);
  Serial.print(" | Status: ");
  
  // 3. Spoilage Logic
  if (gasLevel >= SPOILAGE_THRESHOLD) {
    // ---- SPOILED STATE ----
    Serial.println("SPOILED! (High Gas Concentration)");

    // Turn off 'Fresh' indicator
    digitalWrite(GREEN_LED_PIN, LOW);
    
    // Turn on 'Spoiled' indicator and sound the alarm
    digitalWrite(RED_LED_PIN, HIGH);
    tone(BUZZER_PIN, 2000); // High pitch alarm tone
    
  } else {
    // ---- FRESH STATE ----
    Serial.println("Fresh (Normal)");
    
    // Turn on 'Fresh' indicator
    digitalWrite(GREEN_LED_PIN, HIGH);
    
    // Turn off 'Spoiled' indicator and silence the alarm
    digitalWrite(RED_LED_PIN, LOW);
    noTone(BUZZER_PIN); 
  }
  
  // Wait half a second before taking the next reading
  delay(500);
}
