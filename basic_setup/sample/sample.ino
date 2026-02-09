#define TRIG_PIN 9
#define ECHO_PIN 10

void setup() {
  Serial.begin(115200); 
  pinMode(9, OUTPUT); // Trig
  pinMode(10, INPUT); // Echo
}

void loop() {
  digitalWrite(9, LOW);
  delayMicroseconds(2);
  digitalWrite(9, HIGH);
  delayMicroseconds(10);
  digitalWrite(9, LOW);
  
  long duration = pulseIn(10, HIGH, 30000);
  float distance = (duration == 0) ? -1.0 : (duration * 0.0343 / 2.0);

  // CRITICAL: Must be EXACTLY this format for the Python script
  Serial.print(millis());
  Serial.print(",");
  Serial.println(distance);
  
  delay(50);
}          
 