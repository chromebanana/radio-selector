#include <avr/sleep.h>
#include <avr/power.h>
#include <avr/interrupt.h>

const int rotaryPulsePin = 2;   // Pin connected to rotary pulse switch (generates pulses)
const int dialMotionPin = 3;    // Pin connected to dial motion switch (closes when dial is moving)
volatile bool dialingInProgress = false;  // Track if dialing is currently in progress
volatile int pulseCount = 0;    // Variable to store pulse count (volatile for ISR)
const unsigned long debounceDelay = 100;
const unsigned long preSleepDelay = 100;  

void setup() {
    pinMode(rotaryPulsePin, INPUT_PULLUP);  // Rotary pulse input with internal pull-up
    pinMode(dialMotionPin, INPUT_PULLUP);   // Dial motion input with internal pull-up

    Serial.begin(9600);

    attachInterrupt(digitalPinToInterrupt(dialMotionPin), handleDialMotion, FALLING);
}

void loop() {
    if (dialingInProgress) {
        countPulses();
        if (digitalRead(dialMotionPin) == HIGH) {
            Serial.print("Dialed number: ");
            Serial.println(pulseCount);
            delay(preSleepDelay); // ensure serial.print has time to finish before sleep...
            
            pulseCount = 0; // Reset pulse count for the next dial
            dialingInProgress = false;  // Mark dialing as finished
        }
    } else {
        goToSleep();
    }
}

void goToSleep() {
    set_sleep_mode(SLEEP_MODE_PWR_DOWN);
    sleep_enable();
    
    ADCSRA &= ~(1 << ADEN); // Disable ADC to save power
    power_timer0_disable();  // Disable Timer0 (used for millis() and delay())

    // Go to sleep
    sleep_mode();  // Arduino will wake up here when an interrupt occurs

    sleep_disable();
    ADCSRA |= (1 << ADEN);  // Re-enable ADC after waking up
    power_timer0_enable();
}

void handleDialMotion() {
    // ISR to handle the start and stop of dial motion
    if (digitalRead(dialMotionPin) == LOW) {
        // Dial is in motion
        dialingInProgress = true;
    }
}

void countPulses() {
    int pulseState = digitalRead(rotaryPulsePin);
    if (pulseState == HIGH) {
        pulseCount++;
        delay(debounceDelay);
    }
}