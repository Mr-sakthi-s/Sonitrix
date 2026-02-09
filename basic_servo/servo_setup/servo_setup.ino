#include <Servo.h>

#define TRIG_PIN 8
#define ECHO_PIN 9
#define SERVO_PIN 6

Servo radarServo;

long readDistanceCM() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 25000); // 25ms timeout

  if (duration == 0) return -1;   // no echo

  return duration * 0.034 / 2;
}

void setup() {
  Serial.begin(9600);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  radarServo.attach(SERVO_PIN);
}

void loop() {

  // Forward sweep
  for (int angle = 15; angle <= 165; angle++) {
    radarServo.write(angle);
    delay(30);

    long distance = readDistanceCM();
    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);
  }

  // Backward sweep
  for (int angle = 165; angle >= 15; angle--) {
    radarServo.write(angle);
    delay(30);

    long distance = readDistanceCM();
    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);
  }
}
