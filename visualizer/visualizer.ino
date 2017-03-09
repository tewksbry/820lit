#include <Adafruit_NeoPixel.h>

#define PIN 6
#define NUM_PIXELS 300

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
  BrightEdges = 'e',
  CycleSpeed = 'y',
};

typedef struct{
  uint8_t R;
  uint8_t G;
  uint8_t B;
  uint8_t W;
} COLOR;

typedef struct{
  uint8_t Pos;
  uint8_t V;
  COLOR color;
} BALL;

typedef enum {
  SingleLight = 0,
  Rainbow,
  Random,
  Random_bright,
  Grayscale,
  USC,
  Mood,
} Palette_type;

typedef enum {
  Fill = 0,
  MiddleOut,
  MiddleOutFill,
  Strobe,
  Cycle,
  MiddleOutWHITE,
  Loading,
} Display_type;

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_PIXELS, PIN, NEO_GRB + NEO_KHZ800);

// PARAMETERS
uint8_t volume = 0;
uint8_t prev_volume = 0;
uint8_t frequency = 0;
uint8_t prev_frequency = 0;
float fade = 0.7;
float cutoff = 1;
bool bright_edges = true;
bool dim_center = true;
Palette_type palette = Rainbow;
Display_type display_t = Loading;
COLOR singleLight{255,255,255,255};
int cycle_index = 0;
int cycle_length = 5000;
BALL balls[10];



void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  strip.begin();
  strip.setBrightness(255);
  strip.show();
}


//SERIAL PROCESSING
bool read(char &character, long timeout = 100) {
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
      fade =  (float)character*0.01;
      break;
    case Cutoff:
      if (!read(character)) { return false; }
      cutoff = (float)character*0.01;
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
      if (!read(character)) { return false; }
      singleLight.R = character;
      
      if (!read(character)) { return false; }
      singleLight.G = character;
      
      if (!read(character)) { return false; }
      singleLight.B = character;
      
      if (!read(character)) { return false; }
      singleLight.W = character;
      break;
    case Brightness:
      if (!read(character)) { return false; }
      strip.setBrightness((int)character);
      break;
    case DimCenter:
      if (!read(character)) { return false; }
      dim_center = character != 0;
      break;
    case BrightEdges:
      if (!read(character)) { return false; }
      bright_edges = character != 0;
      break;
    case CycleSpeed:
      if (!read(character)) { return false; }
      cycle_length = character*100;
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

COLOR moodPalette(int i, int len){
  i = normalizeIndex(i, len, 384);
  if (i < 128){
    return COLOR{(uint8_t)(50+i), 10, 128, 0};
  }else if (i < 256){
    i -= 128;
    return COLOR{(uint8_t)(178-i), (uint8_t)(10+i), 128, 0};
  }else if (i < 384){
    i -= 256;
    return COLOR{50, (uint8_t)(138-i), 128, 0};
  }
}

COLOR grayscalePalette(int i, int len){
  i = normalizeIndex(i, len, 255);
  return COLOR{(uint8_t)(i+1), (uint8_t)(i+1), (uint8_t)(i+1), (uint8_t)(i+1)};
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
    case Mood:
      c = moodPalette(i, len);
      break;
  }
  return c;
}


// PATTERN DISPLAYS

void middleOutPattern(){
  uint8_t middle_pixel = NUM_PIXELS/2;
  uint8_t range_size = middle_pixel*cutoff;
  uint8_t active_range = range_size*volume/255.0;
  uint8_t spillover_start = 2 * range_size - middle_pixel;
  uint8_t startwhite = 108;

  for (int i = active_range; i < middle_pixel; i++){
    COLOR c;
    if (display_t == MiddleOutFill){
      c = getColor(active_range, range_size);
      if (dim_center){
        dim(c, (float)(i+1)/(middle_pixel));
      }
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
    if (display_t == MiddleOutWHITE && i >= startwhite){
      c.R = 255;
      c.G = 255;
      c.B = 255;
      c.W = 255;
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

void bounce(){
  
  
}

int loadingI = 0;
int loadingPixNum = 1;

void loading(){
  int jumpAmount = 2;

  for (int i = 0; i < NUM_PIXELS; i++){
      if (i < loadingPixNum*2){
        if (i%2 == 0){
          strip.setPixelColor((loadingI+i) % NUM_PIXELS, colorAsInt(getColor(loadingPixNum, NUM_PIXELS/2)));
        }else{
          strip.setPixelColor((loadingI+i) % NUM_PIXELS, colorAsInt({0,0,0,0}));
        }
      }else{
        strip.setPixelColor((loadingI+i) % NUM_PIXELS, colorAsInt({0,0,0,0}));
      }
  }
  
  loadingI += 3;
  if (loadingPixNum*2 > NUM_PIXELS){
    loadingPixNum = 1;
  }
  if (loadingI >= NUM_PIXELS){
    loadingI = 0;
    loadingPixNum+=jumpAmount;
  }
}

void displayPattern(){
  switch (display_t){
    case Fill:
      fillPalette();
      break;
    case MiddleOut:
    case MiddleOutWHITE:
    case MiddleOutFill:
      middleOutPattern();
      break;
    case Strobe:
      strobe();
      break;
    case Cycle:
      for (int i = 0; i < NUM_PIXELS; i++){
          strip.setPixelColor(i, colorAsInt(getColor(cycle_index, cycle_length)));
      }
      cycle_index++;
      if (cycle_index >= cycle_length){
        cycle_index = 0;
      }
      break;
     case Loading:
      loading();
      break;
  }
}

void loop() {
  Serial.println('*');
  while (Serial.available()){
    if (!handleSerial()){
      strip.setPixelColor(0, 0,0,0,255);
      strip.show();
//      delay(5000);
    }
  }
  displayPattern();
  strip.show();

  prev_volume = volume;
  prev_frequency = frequency;
}
