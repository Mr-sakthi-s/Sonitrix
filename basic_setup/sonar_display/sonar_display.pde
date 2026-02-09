import processing.serial.*;

Serial myPort;

int angle = 0;
int distance = 0;

int maxRange = 40;
float sweepWidth = 6;   // beam thickness

void setup() {
  size(900, 600);
  smooth(8);

  println(Serial.list()); // run once to verify
  myPort = new Serial(this, Serial.list()[0], 115200);
  myPort.bufferUntil('.');
}


void draw() {
  drawBackground();
  drawRadarGrid();
  drawSweep();
  drawObject();
  drawHUD();
}

void serialEvent(Serial p) {
  String data = p.readStringUntil('.');
  if (data == null) return;

  data = trim(data);          // remove whitespace
  data = data.replace(".", "");

  // reject bad frames
  if (!data.contains(",")) return;

  String[] values = split(data, ',');

  if (values.length != 2) return;

  try {
    int a = int(values[0]);
    int d = int(values[1]);

    angle = constrain(a, 0, 180);
    distance = d;

  } catch (Exception e) {
    // silently drop corrupted packet
  }
}

/* ================= VISUALS ================= */

void drawBackground() {
  noStroke();
  fill(0, 25);
  rect(0, 0, width, height);
}

void drawRadarGrid() {
  pushMatrix();
  translate(width / 2, height - 40);

  stroke(0, 180, 0);
  noFill();

  for (int r = 100; r <= 400; r += 100) {
    arc(0, 0, r * 2, r * 2, PI, TWO_PI);
  }

  for (int a = 0; a <= 180; a += 30) {
    float x = 400 * cos(radians(a));
    float y = -400 * sin(radians(a));
    line(0, 0, x, y);
  }

  popMatrix();
}

void drawSweep() {
  pushMatrix();
  translate(width / 2, height - 40);

  for (int i = 0; i < sweepWidth; i++) {
    stroke(0, 255 - i * 30, 0, 180);
    strokeWeight(2);

    float x = 400 * cos(radians(angle - i));
    float y = -400 * sin(radians(angle - i));
    line(0, 0, x, y);
  }

  popMatrix();
}

void drawObject() {
  if (distance <= 0 || distance > maxRange) return;

  float d = map(distance, 0, maxRange, 0, 400);

  pushMatrix();
  translate(width / 2, height - 40);

  stroke(255, 60, 60);
  strokeWeight(6);

  float x = d * cos(radians(angle));
  float y = -d * sin(radians(angle));

  point(x, y);
  popMatrix();
}

void drawHUD() {
  fill(0, 255, 0);
  textSize(18);
  text("ANGLE : " + angle + "°", 20, 30);
  text("DIST  : " + distance + " cm", 20, 55);
}
