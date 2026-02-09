import processing.serial.*;

Serial myPort;
String incomingData;

int angle = 0;
float distance = 0;

void setup() {
  size(800, 500);
  smooth();

  myPort = new Serial(this, "COM12", 9600); // CHANGE COM PORT
  myPort.bufferUntil('\n');
}

void draw() {
  background(0);
  translate(width/2, height);

  drawRadar();
  drawSweep();
  drawObject();
}

void serialEvent(Serial myPort) {
  incomingData = myPort.readStringUntil('\n');
  if (incomingData != null) {
    incomingData = trim(incomingData);
    String[] values = split(incomingData, ',');
    if (values.length == 2) {
      angle = int(values[0]);
      distance = float(values[1]);
    }
  }
}

void drawRadar() {
  stroke(0, 255, 0);
  noFill();

  for (int r = 100; r <= 400; r += 100) {
    arc(0, 0, r * 2, r * 2, PI, TWO_PI);
  }

  for (int a = 0; a <= 180; a += 30) {
    line(0, 0, -400 * cos(radians(a)), -400 * sin(radians(a)));
  }
}

void drawSweep() {
  stroke(0, 255, 0);
  line(0, 0, -400 * cos(radians(angle)), -400 * sin(radians(angle)));
}

void drawObject() {
  if (distance > 0 && distance < 200) {
    float mapped = map(distance, 0, 200, 0, 400);
    stroke(255, 0, 0);
    strokeWeight(6);
    point(-mapped * cos(radians(angle)), -mapped * sin(radians(angle)));
    strokeWeight(1);
  }
}
