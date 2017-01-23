#include <Adafruit_NeoPixel.h>

#define PIN 6
#define NUM_PIXELS 240

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_PIXELS, PIN, NEO_GRBW + NEO_KHZ800);

// Parameters
uint8_t volume = 0;
uint8_t prev_volume = 0;
uint8_t frequency = 0;
uint8_t prev_frequency = 0;
float fade = 0.7;
float cutoff = 0.7;
bool fill = false;
 

enum Params {
  Volume = 'v',
  Frequency = 'f',
};

typedef struct{
  uint8_t R;
  uint8_t G;
  uint8_t B;
  uint8_t W;
} COLOR;

bool read(char &character, long timeout = 1000) {
  long start = millis();
  while (!Serial.available()) {
    if (millis() - start > timeout) {
      return false;
    }
  }
  character = Serial.read();
  return true;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  strip.begin();
//  strip.setPixelColor(3, 0,0,255,255);
  strip.show();
}

bool handleSerial(){
  char character;
  if (!read(character) || character != ':') { return false; }
  if (!read(character)) { return false; }

  switch(character) {
    case Volume:
      if (!read(character)) { return false; }
      volume = character;
    case Frequency:
      if (!read(character)) { return false; }
      frequency = character;
  }
}

uint32_t colorAsInt(const COLOR &c){
  return ((uint32_t)c.W << 24) | ((uint32_t)c.R << 16) | ((uint32_t)c.G <<  8) | c.B;
}

void dim(COLOR &c, float f){
   c.R *= f;
   c.G *= f;
   c.B *= f;
   c.W *= f;
}

COLOR getRGBW(uint32_t color){
   COLOR c;
   c.R = color >> 16;
   c.G = color >> 8;
   c.B = color;
   c.W = color >> 24;
   return c;
}




void middleOutPattern(){
  for (int i = 0; i < NUM_PIXELS; i++){
    COLOR c = getRGBW(strip.getPixelColor(i));
    dim(c, 0.7);
    strip.setPixelColor(i, colorAsInt(c));
  }

  uint8_t volumeRange = volume*NUM_PIXELS*0.01*0.5;
  uint8_t middlePixel = NUM_PIXELS/2;
  for (int i = 0; i < volumeRange; i++){
    strip.setPixelColor(middlePixel+i, 0,0,0,255);
    strip.setPixelColor(middlePixel-i -1, 0,0,0,255);
  }
}

void fillColor(const COLOR& c){
  for (int i = 0; i < NUM_PIXELS; i++){
      strip.setPixelColor(i, c.R, c.G, c.B, c.W);
    }
}


void strobe(bool colored = false){
  if (strip.getPixelColor(0)){
    strip.clear();
    return;
  }
  
  COLOR c;
  if (colored){
    c.R = random(0, 256);
    c.G = random(0, 256);
    c.B = random(0, 256);
  }else{
    c.W = 255;
  }
  fillColor(c);
  
}

void loop() {
  strip.setBrightness(50);
  while (Serial.available()){
    handleSerial();
  }
  middleOutPattern();
//  strobe();
//  strobe(true);
  strip.show();
  delay(30);

  prev_volume = volume;
  prev_frequency = frequency;
}
