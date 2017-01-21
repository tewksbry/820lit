
#include <Adafruit_NeoPixel.h>
#define PIN 6

uint32_t lightRGB[240];
uint32_t lightRGB_n[960];
bool updated = true;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(240, PIN, NEO_RGBW + NEO_KHZ800);
int color = 1;

void setup() {
  // put your setup code here, to run once:
  Serial.setTimeout(1);
  Serial.begin(9600);
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
}

void loop() {
  // put your main code here, to run repeatedly:
  int pixel = 0;
  int R = -1;
  int G = -1;
  int B = -1;
  int W = -1;
  while(pixel < 960){
    
    
    if (Serial.available()){
//      Serial.write(Serial.available());
      // fill array
      if (R == -1){
        R = Serial.read();
      }else if (G == -1){
        G = Serial.read();
      }else if (B == -1){
        B = Serial.read();
      }else{
        W = Serial.read();
        strip.setPixelColor(pixel, strip.Color(R, G, B, W));
        R, G, B, W = -1, -1, -1, -1;
      }
//      strip.setPixelColor(pixel, strip.Color(color,color,color,color));
//      color++;
      pixel++;
      
//      for (int i = 0; i < 240; i++){
//          int R = Serial.read();
//          int G = Serial.read();
//          int B = Serial.read();
//          int W = Serial.read();
//  //      strip.setPixelColor(i, strip.Color(Serial.read(),Serial.read(),Serial.read(),Serial.read()));
//          strip.setPixelColor(i, strip.Color(color,color,color,color));
//  //      lightRGB_n[i] = Serial.read();
//          color++;
//      }
    }
  }
  strip.show();
//  if (updated){
//    for(int i=0; i<strip.numPixels(); i++) {
////      strip.setPixelColor(i, strip.Color(color,color,color,color));
//      strip.setPixelColor(i, lightRGB[i]);
//    }
//    strip.show();
//    updated = false;
//    color++;
//    delay(10);
//  }
}

void serialEvent()
{
//  int lightRGB_n[960] = Serial.read;
//  Serial.readBytes(lightRGB_n, 960); 
//  lightRGB_n = 
////  Serial.write((byte)2);
//  for (int i = 0; i < 240; i++){
//    
//    lightRGB[i] = strip.Color((uint32_t)lightRGB_n[i*4], (uint32_t)lightRGB_n[i*4+1], (uint32_t)lightRGB_n[i*4+2], (uint32_t)lightRGB_n[i*4+3]);
//    Serial.write((byte)lightRGB[i]);
////    lightRGB[i] = ((uint32_t)lightRGB[i*4+3] << 24) | ((uint32_t)lightRGB[i*4] << 16) | ((uint32_t)lightRGB[i*4+1] <<  8) | lightRGB[i*4+2];
//  }
//  updated = true;
}
