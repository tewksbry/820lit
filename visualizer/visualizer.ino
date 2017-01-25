#include <Adafruit_NeoPixel.h>

#define PIN 6
#define NUM_PIXELS 240

enum Params {
  Volume = 'v',
  Frequency = 'f',
  Palette = 'p',
  Fade = 'a',
  Cutoff = 'c',
  Display = 'd',
  LightColor = 'l',
  Brightness = 'b',
  DimCenter = 's',
  BrightEdges = 'e'
};

typedef struct{
  uint8_t R;
  uint8_t G;
  uint8_t B;
  uint8_t W;
} COLOR;

typedef enum {
  SingleLight = 0,
  Rainbow,
  Random,
  Random_bright,
  Grayscale,
  USC
} Palette_type;

typedef enum {
  Fill = 0,
  MiddleOut,
  MiddleOutFill,
  Strobe,
} Display_type;

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_PIXELS, PIN, NEO_GRBW + NEO_KHZ800);

// PARAMETERS
uint8_t volume = 0;
uint8_t prev_volume = 0;
uint8_t frequency = 0;
uint8_t prev_frequency = 0;
float fade = 0.7;
float cutoff = 1;
bool bright_edges = true;
bool dim_center = true;
Palette_type palette = USC;
Display_type display_t = Fill;
COLOR singleLight{0, 0, 0, 0};
 
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  strip.begin();
  strip.show();
}


//SERIAL PROCESSING
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
    case Palette:
      if (!read(character)) { return false; }
      palette = (Palette_type)(int)character;
      break;
    case Fade:
      if (!read(character)) { return false; }
      fade = character/100.0;
      break;
    case Cutoff:
      if (!read(character)) { return false; }
      cutoff = character/100.0;
      break;
    case Display:
      if (!read(character)) { return false; }
      display_t = (Display_type)(int)character;
      break;
    case LightColor:
      singleLight.R = 0;
      singleLight.G = 0;
      singleLight.B = 0;
      singleLight.W = 0;
      if (!read(character)) { 
//        strip.setPixelColor(10, 0, 0, 0, 255);
        return false; }
      singleLight.R = character;
//      strip.setPixelColor(character, 255, 0, 0, 0);
      
      if (!read(character)) { 
//        strip.setPixelColor(20, 0, 0, 0, 255);
        return false; }
      singleLight.G = character;
//      strip.setPixelColor(character, 0, 255, 0, 0);
      
      if (!read(character)) { 
//        strip.setPixelColor(30, 0, 0, 0, 255);
        return false; }
      singleLight.B = character;
//      strip.setPixelColor(character, 0, 0, 255, 0);
      
      if (!read(character)) { 
//        strip.setPixelColor(40, 0, 0, 0, 255);
        return false; }
      singleLight.W = character;
//      strip.setPixelColor(character, 0, 0, 0, 255);
//      strip.show();
//      delay(5000);
      
      break;
    case Brightness:
      if (!read(character)) { return false; }
      strip.setBrightness(character);
      break;
    case DimCenter:
      if (!read(character)) { return false; }
      if (character == 'Y' || character == 'y' || character == 'N' || character == 'n'){
        dim_center = (character == 'Y' || character == 'y');
      }else{
        dim_center = character;
      }
      break;
    case BrightEdges:
      if (!read(character)) { return false; }
      if (character == 'Y' || character == 'y' || character == 'N' || character == 'n'){
        bright_edges = (character == 'Y' || character == 'y');
      }else{
        bright_edges = character;
      }
      break;
  }
  return true;
}

//HELPER FUNCTIONS
 
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
  return (i % len)*fullLen/len;
}


//PALETTES

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

COLOR USCPalette(int i, int len){
  len = 20;
  i = i % len;
  
  COLOR r{255, 0, 0, 0};
  COLOR y{255, 70, 0, 0};
  
  if (i < len/2){
    return r;
  }else{
    return y;
  }
}

COLOR grayscalePalette(int i, int len){
  i = normalizeIndex(i, len, 255);
  return COLOR{0, 0, 0, (uint8_t)(i+1)};
}


COLOR getColor(int i, int len){
  COLOR c;
  switch (palette){
    case SingleLight:
      c = singleLight;
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
      break;
    case USC:
      c = USCPalette(i, len);
      break;
  }
  return c;
}


// PATTERN DISPLAYS

void middleOutPattern(){
  uint8_t middle_pixel = NUM_PIXELS/2;
  uint8_t range_size = middle_pixel*cutoff;
  uint8_t active_range = range_size*0.01*volume;
  uint8_t spillover_start = 2 * range_size - middle_pixel;

  for (int i = active_range; i < middle_pixel; i++){
    COLOR c;
    if (display_t == MiddleOutFill){
      c = getRGBW(strip.getPixelColor(middle_pixel+active_range));
//      if (dim_center){
//        dim(c, (float)(i+1)/(middle_pixel));
//      }
    }else{
      c = getRGBW(strip.getPixelColor(middle_pixel+i));
      dim(c, fade);
    }
    strip.setPixelColor(middle_pixel+i, colorAsInt(c));
    strip.setPixelColor(middle_pixel-i -1, colorAsInt(c));
  }
  for (int i = 0; i < active_range; i++){
    COLOR c = getColor(frequency, 100);
    if (bright_edges){
      c.W = 255*i/range_size/5;
    }
    if (dim_center){
      dim(c, (float)(i+1)/(range_size));
    }
    strip.setPixelColor(middle_pixel + i, colorAsInt(c));
    strip.setPixelColor(middle_pixel - i - 1, colorAsInt(c));
    
    if ( i >= spillover_start){
      uint8_t spillover = i - spillover_start;
      strip.setPixelColor(NUM_PIXELS - spillover - 1, colorAsInt(c));
      strip.setPixelColor(spillover, colorAsInt(c));
    }
  }
}

void fillPalette(){
  for (int i = 0; i < NUM_PIXELS; i++){
      strip.setPixelColor(i, colorAsInt(getColor(i, NUM_PIXELS)));
  }
}

void strobe(){
  delay(30);
  if (strip.getPixelColor(0)){
    strip.clear();
    return;
    
  }
  fillPalette();
}

void displayPattern(){
  switch (display_t){
    case Fill:
      fillPalette();
      break;
    case MiddleOut:
    case MiddleOutFill:
      middleOutPattern();
      break;
    case Strobe:
      strobe();
      break;
  }
}

void loop() {
  strip.setBrightness(255);
  while (Serial.available()){
    if (!handleSerial()){
      strip.setPixelColor(0, 0,0,0,255);
      strip.show();
      delay(5000);
    }
  }
  displayPattern();
  strip.show();

  prev_volume = volume;
  prev_frequency = frequency;
}
