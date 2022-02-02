#include <Arduino.h>

#include <SPI.h>
#include <SD.h>
#include <wire.h>

// NRF radio stuff
#include <nRF24L01.h>
#include <RF24.h>

// Make SD card object, tell it what SPI sel pin to use
File SD_file;
const int chipSelect = 10;

// Break program when button pushed
const int endLoopPin = 3;

// MPU6050 Stuff
// follow this tutorial https://howtomechatronics.com/tutorials/arduino/arduino-and-mpu6050-accelerometer-and-gyroscope-tutorial/
const int MPU = 0x68; // MPU6050 I2C address
int c = 0;

RF24 radio(7, 8); // CE, CSN

const byte address[6] = "00001";

byte* dataMem[20];

void setup() {
  //Start Serial
  Serial.begin(115200); 
  Serial.println("Starting up!");

  //Init buttons
  pinMode(endLoopPin, INPUT_PULLUP);

  if (!SD.begin()) { // Start SD and stop if there is not one connected
    Serial.println("Initialization failed :(");
    return;
  }

  Serial.println("SD Card Mounted!");

  SD.remove("data.hex"); // Delete old file from last run

  SD_file = SD.open("data.hex", FILE_WRITE);  // Open new file
  
  //Init MPU6050
  Wire.begin();                      // Initialize comunication
  Wire.beginTransmission(MPU);       // Start communication with MPU6050 // MPU=0x68
  Wire.write(0x6B);                  // Talk to the register 6B
  Wire.write(0x00);                  // Make reset - place a 0 into the 6B register
  Wire.endTransmission(true);        // End the transmission

  // Init NRF24L01
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();

  Serial.println("Beginning Data Collection");
}

// Set of values to read inputs to in memory
unsigned long  read_unsigned_long;
unsigned short read_unsigned_short;

void loop() {
  // Get time value
  *((unsigned long*)(dataMem) +0) = micros(); // Read time
  *((unsigned short*)(dataMem) +2) = analogRead(7); // Read gas pedal

  // Serial.print(micros());
  // Serial.print(" ");
  // Serial.println(*(unsigned long*)(dataMem +0));

  // Get IMU acceleration data
  Wire.beginTransmission(MPU);
  Wire.write(0x3B); // 0x3B is ACCEL_XOUT_H, 
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 6, true); // request to read 6 bytes from MPU

  // Each is a 2s comp short int
  // Directly copying data to internal buffer, 
  // no need to process yet, use python to actually do math, for now just go fast
  for(size_t ii=0; ii<3; ii++){
    *(dataMem +3 +ii) = (Wire.read() << 8 | Wire.read()); //Read two bytes
  }
  
  // Get IMU gyroscope data
  Wire.beginTransmission(MPU);
  Wire.write(0x43); // 0x43 is the Gyro X register
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 6, true); // request to read 6 bytes from MPU

  // Each is a 2s comp short int
  // Directly copying data to internal buffer, 
  // no need to process yet, use python to actually do math, for now just go fast
  for(size_t ii=0; ii<3; ii++){
    *(dataMem +6 +ii) = (Wire.read() << 8 | Wire.read()); //Read two bytes
  }

  
  // Send data

  // Write whole array
  SD_file.write((char*)dataMem, 20);
  // SD_file.flush();

  // Write val to nextium
  // Serial.print("speed.val=");
  // Serial.print(read_unsigned_short);
  // Serial.write(0xFF);
  // Serial.write(0xFF);
  // Serial.write(0xFF);
  
  radio.write((char*)dataMem, 20);



  //check for loop exit
  if(!digitalRead(endLoopPin)){ //Check once
    if(!digitalRead(endLoopPin)){ //Check again, confirm input
      SD_file.close();
      Serial.println("All done!");
      Serial.end();
      delay(100);
      exit(0);
    } 
  }
}