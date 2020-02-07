#include <Adafruit_CircuitPlayground.h>

bool leftButtonPressed;
bool rightButtonPressed;
bool slideSwitch;

float X, Y, Z;
String buf;
uint8_t pixel_pointer = 0;
uint32_t pixel_set_word;
int sa,i;

unsigned char atoh (unsigned char data) // Convert ASCII to Hex Digit (4 bit nibble)
 { if (data > '9') 
    { data += 9;
    }
    data = data & 0x0F;
    return (data);
 }

void setup() {
  Serial.begin(9600);
  CircuitPlayground.begin();
  CircuitPlayground.clearPixels();
}

void loop() {
  X = CircuitPlayground.motionX();
  Y = CircuitPlayground.motionY();
  Z = CircuitPlayground.motionZ();
  leftButtonPressed = CircuitPlayground.leftButton();
  rightButtonPressed = CircuitPlayground.rightButton();
  slideSwitch = CircuitPlayground.slideSwitch();
  if (slideSwitch){
     Serial.print("X: ");
     Serial.print(X);
     Serial.print("  Y: ");
     Serial.print(Y);
     Serial.print("  Z: ");
     Serial.print(Z);
     Serial.print("  Buttons: ");
     if (leftButtonPressed) {
       Serial.print("1 ");
     } 
     else {
       Serial.print("0 ");
     }
     if (rightButtonPressed) {
        Serial.print("1 ");
        } 
     else {
          Serial.print("0 ");    
        }
     Serial.println(" ");
  }
  if(Serial.available() > 7 ){
     buf=Serial.readString();
     pixel_pointer = atoh(buf[0]);
     pixel_set_word=0;
     for (i=1;i<7;i++){
         pixel_set_word *= 16;
         pixel_set_word += atoh(buf[i]);
     }
     if (pixel_pointer < 10){
          CircuitPlayground.setPixelColor(pixel_pointer, pixel_set_word);
     }
     else {
          for (i=0;i<10;i++){
            CircuitPlayground.setPixelColor(i, pixel_set_word);
        }
     }
   }
   delay(10);
}
