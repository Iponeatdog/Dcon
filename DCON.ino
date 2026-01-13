#include <dummy.h>

// const int adcPin = A0;          // Use A0
// const unsigned long Ts = 1000;  // Sampling period in µs (1000 µs = 1 kHz)

// unsigned long lastSample = 0;

// void setup() {
//   Serial.begin(9600);
//   analogReadResolution(12);   // UNO R4 supports 12-bit ADC
// }

// void loop() {
//   unsigned long now = micros();

//   if (now - lastSample >= Ts) {
//     lastSample += Ts;

//     int sample = analogRead(adcPin);
//     Serial.println(sample);
//   }
// }

// ESP32
const int analogPin = 1; // ADC1 Channel 6 (GPIO34)
const int ledPin = 13;
const int butPin = 2; // Button

int measure = 0;

void setup() {
  Serial.println("Channel 1");
  pinMode(ledPin, OUTPUT);
  Serial.begin(57600);
}

void loop() {
  int sensorValue = analogRead(analogPin); // Reads 0-4095
  // Convert to voltage (0.0V - 3.3V)
  // float voltage = sensorValue * (3.3 / 4095.0);
  // float fixV = (voltage - 0.0405) / 1.0674
  float fixa = (sensorValue-50.846)/1.0671 * (3.3/4095.0);
  if(fixa < 0){
    fixa = 0;
  }

  // Serial.println(voltage);
  // Serial.println(sensorValue);
  // Serial.println(fixa);

  int isPress = digitalRead(butPin);

  // Serial.println(isPress);

  if(isPress && measure){
    measure = 0;
    digitalWrite(ledPin, LOW);
    Serial.println("END");
    delay(1000);
  }
  else if(isPress && !measure){
    measure = 1;
    digitalWrite(ledPin, HIGH);
    delay(1000);
  }

  if(measure){
    Serial.println(fixa);
  }
  delay(8);
}


