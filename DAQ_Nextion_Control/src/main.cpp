#include <Arduino.h>

// We assigned a name LED pin to pin number 22
// this will assign the name PushButton to pin numer 15
const int TopBTN = 2;
const int LeftBTN = 3;
const int RightBTN = 4;
const int BottomBTN = 5;
const int SelectBTN = 6;
// This Setup function is used to initialize everything 
void setup() {
  // This statement will declare pin 22 as digital output 
  // This statement will declare pin 15 as digital input 
  Serial.begin(9600);
  //Serial.print("bauds=115200");
  //Serial.write(0xff);  // We always have to send this three lines after each command sent to nextion.
  //Serial.write(0xff);
  //Serial.write(0xff);
  pinMode(TopBTN, INPUT_PULLUP);
}

void loop() {

  // digitalRead function stores the 
  // in variable push_button_state
  int SelectState = digitalRead(SelectBTN);
  int TopState = digitalRead(TopBTN);
  int LeftState = digitalRead(LeftBTN);
  int RightState = digitalRead(RightBTN);
  int BottomState = digitalRead(BottomBTN);

  int variable1 = 22;
  int variable2 = 10;
  // if condition checks if push button is pressed
  // if pressed LED will turn on otherwise remain off 
  if (SelectState == HIGH) {
    //enter button on nextion
    Serial.print("va0.val=");  // This is sent to the nextion display to set what object name (before the dot) and what atribute (after the dot) are you going to change.
    Serial.print(variable1);  // This is the value you want to send to that object and atribute mention before.
    Serial.write(0xff);  // We always have to send this three lines after each command sent to the nextion display.
    Serial.write(0xff);
    Serial.write(0xff);
  } else if (TopState == HIGH ) { 

  } else if (LeftState == HIGH) {
     
  } else if (RightState == HIGH) {
  
  } else if (LeftState == HIGH) {

  }



}