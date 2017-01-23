#include <Adafruit_NeoPixel.h>

#define PIN 6
#define NUM_PIXELS 240

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

typedef enum {
  White = 0,
  Rainbow,
  Random,
  Random_bright,
  Grayscale
} Palette_type;

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_PIXELS, PIN, NEO_GRBW + NEO_KHZ800);

// Parameters
uint8_t volume = 0;
uint8_t prev_volume = 0;
uint8_t frequency = 50;
uint8_t prev_frequency = 0;
float fade = 0.5;
float cutoff = 1;
bool fill = false;
Palette_type palette = Random;
 



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
      break;
    case Frequency:
      if (!read(character)) { return false; }
      frequency = character;
      break;
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

int normalizeIndex(long i, int len, int fullLen){
  return i*fullLen/len;
}

COLOR rainbowPalette(int i, int len){
  i = normalizeIndex(i, len, 768);
  if (i < 256){
    return COLOR{(uint8_t)(255-i), (uint8_t)i, 0, 0};
  }else if (i < 512){
    i -= 256;
    return COLOR{0, (uint8_t)(255-i), (uint8_t)i, 0};
  }else{
    i -= 512;
    return COLOR{ (uint8_t)i, 0,(uint8_t)(255-i), 0};
  }
}

COLOR grayscalePalette(int i, int len){
  i = normalizeIndex(i, len, 255);
  return COLOR{0, 0, 0, (uint8_t)(i+1)};
}


COLOR getColor(int i, int len){
  COLOR c;
  switch (palette){
    case White:
      c = COLOR{255,255,255,255};
      break;
    case Rainbow:
      c = rainbowPalette(i, len);
      break;
    case Random:
      c = COLOR{(uint8_t)random(0, 256), (uint8_t)random(0, 256), (uint8_t)random(0, 256), 0};
      break;
    case Random_bright:
      c = COLOR{(uint8_t)random(0, 256), (uint8_t)random(0, 256), (uint8_t)random(0, 256), (uint8_t)random(0, 256)};
      break;
    case Grayscale:
      c = grayscalePalette(i, len);
  }
  return c;
}


void middleOutPattern(){
  for (int i = 0; i < NUM_PIXELS; i++){
    COLOR c = getRGBW(strip.getPixelColor(i));
    dim(c, fade);
    strip.setPixelColor(i, colorAsInt(c));
  }

  uint8_t middlePixel = NUM_PIXELS/2;
  uint8_t volumeRange = middlePixel*0.01*volume;
  uint8_t color = colorAsInt(getColor(frequency, 100));
  for (int i = 0; i < volumeRange; i++){
    COLOR c = getColor(i, middlePixel);
    dim(c, (float)(i+1)/(middlePixel+1));
    strip.setPixelColor(middlePixel+i, colorAsInt(c));
    strip.setPixelColor(middlePixel-i -1, colorAsInt(c));
//    strip.setPixelColor(middlePixel+i, color);
//    strip.setPixelColor(middlePixel-i -1, color);
  }
}

void fillPalette(){
  for (int i = 0; i < NUM_PIXELS; i++){
      strip.setPixelColor(i, colorAsInt(getColor(i, NUM_PIXELS)));
  }
}

void fillColor(const uint32_t& c){
  for (int i = 0; i < NUM_PIXELS; i++){
      strip.setPixelColor(i, c);
    }
}


void strobe(bool fromPalette = false){
  delay(30);
  if (strip.getPixelColor(0)){
    strip.clear();
    return;
    
  }
  
  if (fromPalette){
    fillPalette();
  }else{
    fillColor(colorAsInt(getColor(0,0)));
  }
}

void loop() {
//  strip.setBrightness(50);
  while (Serial.available()){
    handleSerial();
  }
//  fillPalette();
  middleOutPattern();
//  strobe();
//  strobe(true);
  strip.show();
//  delay(30);

  prev_volume = volume;
  prev_frequency = frequency;
}
