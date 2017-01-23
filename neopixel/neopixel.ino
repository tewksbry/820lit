#include <Adafruit_NeoPixel.h>

#define PIN 6
Adafruit_NeoPixel strip = Adafruit_NeoPixel(240, PIN, NEO_GRBW + NEO_KHZ800);
int currentPixel = -1;
int colorNum = -1;
uint8_t colors[960];
/*
\r  Start of command
\n  End of command
s  show
c  setPixelColor pixelH pixelL red green blue
b  setBrightness brightness
g  getPixelColor pixelH pixelL
n  numPixels
*/

enum Commands {
  Show = 's',
  SetColor = 'c',
  SetBrightness = 'b',
  GetColor = 'g',
  NumberPixels = 'n' 
};

void setup() {
  Serial.begin(115200);
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
//  Serial.println("Ok");
}

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

bool setColor() {
  char character;
  uint8_t pixel;
  uint8_t color[4];

  if (!read(character)) { return false; }
  pixel = (uint8_t) character;
//  if (!read(character)) { return false; }
//  pixel = (uint16_t) character << 8;
//  if (!read(character)) { return false; }
//  pixel += (uint8_t)character;
  if (!read(character)) { return false; }
  color[0] = character;
  if (!read(character)) { return false; }
  color[1] = character;
  if (!read(character)) { return false; }
  color[2] = character;
  if (!read(character)) { return false; }
  color[3] = character;
//  Serial.print("  ");
//  Serial.print(color[0]);
//  Serial.print("  ");
//  Serial.print(color[1]);
//  Serial.print("  ");
//  Serial.print(color[2]);
//  Serial.print("  ");
//  Serial.print(color[3]);
//  Serial.print("  ");

  strip.setPixelColor(pixel, color[0], color[1], color[2], color[3]);
  return true;
}

void loop() {
//  strip.show();
}

//void serialEvent()
//{
//  if (Serial.available()) {
//    char character;
//    if (!read(character) || character != ':') { return; }
////    if (!read(character)) { return; }
////
////    uint8_t command_index = (uint8_t)character;
////    Serial.print(command_index);
//
//    if (!read(character)) { return; }
//
//    switch(character) {
//      case Show:
//        strip.show();
////        Serial.println("Ok");
//        break;
//      case SetColor:
//        if (setColor()) {
////          Serial.println("Ok");
//        } else {
////          Serial.println("Err");
//        }
//        break;
//      case SetBrightness:
//        break;
//      case GetColor:
//        break;
//      case NumberPixels:
////        Serial.println(strip.numPixels());
//        break;
//    }
//  }
//}

void sendOk(char c){
  Serial.println(c);
}
//void serialEvent()
//{
//  if (currentPixel == -1){
//    if (Serial.available()){
//      char character;
////      currentPixel = 0;
//      if (!read(character) || character != ':') { return; }
////      sendOk(character);
//      currentPixel = 0;
//    }
//  } 
//  while (currentPixel >= 0 && Serial.available() >= 4) {
//    char character;
//    uint8_t color[4];
////    Serial.readBytes(color, 4);
//    if (!read(character)) { return false; }
//    if (character == ':') { currentPixel = 0; strip.show(); return;}
//    color[0] = character;
//    if (!read(character)) { return false; }
//    if (character == ':') { currentPixel = 0; strip.show(); return;}
//    color[1] = character;
//    if (!read(character)) { return false; }
//    if (character == ':') { currentPixel = 0; strip.show(); return;}
//    color[2] = character;
//    if (!read(character)) { return false; }
//    if (character == ':') { currentPixel = 0; strip.show(); return;}
//    color[3] = character;
////    Serial.print(currentPixel);
////    Serial.print(color[0]);
////    Serial.print(color[1]);
////    Serial.print(color[2]);
////    Serial.println(color[3]);
//    strip.setPixelColor(currentPixel, color[0], color[1], color[2], color[3]);
//    currentPixel++;
//    if (currentPixel > 255){
//      currentPixel = -1;
//      strip.show();
//    }
////    Serial.println("success");
//  }
//}


void updateColors(){
  for (int i = 0; i < 240; i++){
    sendOk(colors[4*i]);
    sendOk(colors[4*i+1]);
    sendOk(colors[4*i+2]);
    sendOk(colors[4*i+3]);
    strip.setPixelColor(i, colors[4*i], colors[4*i+1], colors[4*i+2], colors[4*i+3]);
  }
  strip.show();
}

void serialEvent()
{
  if (colorNum == -1){
    if (Serial.available()){
      char character;
      if (!read(character) || character != ':') { return; }
      colorNum = 0;
    }
  } 
  if (colorNum >= 0 && Serial.available()) {
    char character;
    if (!read(character)) { return false; }
    if (character == ':') { colorNum = 0; updateColors(); return;}
    
    colors[colorNum] = character;
    colorNum++;
    if (colorNum >= 960){
      colorNum = -1;
      updateColors();
    }
    
  }
}
