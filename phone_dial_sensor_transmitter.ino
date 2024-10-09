const int rotaryPin = 2;    // Pin connected to rotary dial
int pulseCount = 0;         // Variable to store pulse count
bool pulseInProgress = false; // Track if a pulse is currently being detected
unsigned long lastPulseTime = 0;  // Time of the last pulse
const unsigned long debounceDelay = 100;  // Debounce delay (in ms)
const unsigned long pulseEndDelay = 500; // Time to wait after the last pulse (to detect end of dialing)

void setup() {
    // Set D2 as input with internal pull-up enabled
    pinMode(rotaryPin, INPUT_PULLUP);

    // Start serial communication for debugging
    Serial.begin(9600);
}

void loop() {
    // Read the state of the rotary dial pin
    int state = digitalRead(rotaryPin);

    // Check if a pulse is detected (pin goes HIGH)
    if (state == HIGH && !pulseInProgress) {
        pulseCount++;  // Increment the pulse count
        pulseInProgress = true;  // Mark that a pulse is in progress
        lastPulseTime = millis();  // Record the time of the pulse
        delay(debounceDelay);  // Debounce delay to avoid false reads
    }
    
    // If the pin returns to LOW, mark the pulse as completed
    if (state == LOW && pulseInProgress) {
        pulseInProgress = false;
        lastPulseTime = millis();  // Update the time to ensure end-of-pulse delay is accurate
    }

    // Check if enough time has passed since the last pulse (i.e., the dial has stopped)
    if ((millis() - lastPulseTime) > pulseEndDelay && pulseCount > 0) {
        // Print the total number of pulses detected (i.e., the dialed number)
        Serial.print("Dialed number: ");
        Serial.println(pulseCount);

        // Reset pulse count for the next dial
        pulseCount = 0;
    }
}
