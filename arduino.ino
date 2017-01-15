
#include <Adafruit_NeoPixel.h>
#define PIN 6

uint32_t lightRGB[240];
bool updated = true;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(60, PIN, NEO_RGBW + NEO_KHZ800);

void setup() {
  // put your setup code here, to run once:
  Serial.setTimeout(1);
  Serial.begin(9600);
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
}

void loop() {
  // put your main code here, to run repeatedly:
  if (updated){
    for(int i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, lightRGB[i]);
    }
    strip.show();
    updated = false;
  }
}

void serialEvent()
{
  byte lightRGB[960];
  Serial.readBytes(lightRGB, 960); 
  for (int i = 0; i < 240; i++){
    lightRGB[i] = ((uint32_t)lightRGB[i*4+3] << 24) | ((uint32_t)lightRGB[i*4] << 16) | ((uint32_t)lightRGB[i*4+1] <<  8) | lightRGB[i*4+2];
  }
  updated = true;
}
