#include <Servo.h>

#define trigPin 9
#define echoPin 10
#define servoPin 6

Servo myServo;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
  myServo.attach(servoPin);
}

long getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000);
  long distance = duration * 0.034 / 2;

  return distance;
}

void loop() {
  for (int angle = 15; angle <= 165; angle++) {
    myServo.write(angle);
    delay(20);

    long distance = getDistance();

    Serial.print(angle);
    Serial.print(",");
    Serial.print(distance);
    Serial.print(".");
  }

  for (int angle = 165; angle >= 15; angle--) {
    myServo.write(angle);
    delay(20);

    long distance = getDistance();

    Serial.print(angle);
    Serial.print(",");
    Serial.print(distance);
    Serial.print(".");
  }
}
