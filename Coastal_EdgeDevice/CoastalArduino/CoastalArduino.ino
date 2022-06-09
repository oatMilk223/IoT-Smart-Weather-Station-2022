//bme lib imports
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP280.h>
//define sea level pressure 
#define SEALEVELPRESSURE_HPA (1013.25)
//define bme class
Adafruit_BMP280 bmp; // I2C
//led pin setup
int waterR=2;
int waterG=4;
int waterY=3;

int changeR=5;
int changeY=6;
int changeG=7;
int currentR = 8;
int currentY = 9;
int currentG = 10;
char conditionalData;
char conditionalDataWater;

void setup() {
  pinMode(waterR, OUTPUT);
  pinMode(waterG, OUTPUT);
  pinMode(waterY, OUTPUT);
  pinMode(changeR, OUTPUT);
  pinMode(changeG, OUTPUT);
  pinMode(changeY, OUTPUT);
  pinMode(currentR, OUTPUT);
  pinMode(currentY, OUTPUT);
  pinMode(currentG, OUTPUT);
  Serial.begin(9600);
  //bme init
  bool status;
  status = bmp.begin(0x76);
    if (!status) {
      Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
    }
}

void waterValues() {
  if (Serial.available()) {
     conditionalDataWater = Serial.read();
  }
  switch(conditionalDataWater) {
    case 'l':
      digitalWrite (waterR,LOW);
      digitalWrite(waterG,HIGH);
      digitalWrite(waterY,LOW);
      break;
    case 'm':
      digitalWrite (waterG,LOW);
      digitalWrite (waterR,LOW);
      digitalWrite (waterY,HIGH);
      break;
    case 'h':
      digitalWrite (waterR,HIGH);
      digitalWrite (waterY,LOW);
      digitalWrite (waterG,LOW);
      break;
    default:
      digitalWrite (waterY,LOW);
      digitalWrite (waterR,LOW);
      digitalWrite (waterG,LOW);
      break;
  } 
}

void pressureValues() {
  if (Serial.available()) {
     conditionalData = Serial.read();
  }
  switch (conditionalData) {
    case '0':
      //TURN OFF
      digitalWrite(currentR, LOW);
      digitalWrite (currentG,LOW);
      digitalWrite (currentY,LOW);
      digitalWrite (changeY,LOW);
      digitalWrite (changeR,LOW); 
      digitalWrite (changeG,LOW); 
      break;
    case '1':
      digitalWrite (currentR,HIGH);
      digitalWrite (changeG,HIGH);
      //TURN OFF
      digitalWrite (currentG,LOW);
      digitalWrite (currentY,LOW);
      digitalWrite (changeY,LOW);
      digitalWrite (changeR,LOW);  
      break;
    case '2':
      //TURN ON
      digitalWrite (currentR,HIGH);
      digitalWrite (changeY,HIGH);
      //TURN OFF
      digitalWrite (currentG,LOW);
      digitalWrite (currentY,LOW);
      digitalWrite (changeG,LOW);
      digitalWrite (changeR,LOW);   
      break;
    case '3':
      //TURN ON
      digitalWrite (currentR,HIGH);
      digitalWrite (changeR,HIGH);
      //TURN OFF
      digitalWrite (currentG,LOW);
      digitalWrite (currentY,LOW);
      digitalWrite (changeY,LOW);
      digitalWrite (changeG,LOW);   
      break;
    case '4':
      //TURN ON
      digitalWrite (currentY,HIGH);
      digitalWrite (changeY,HIGH);
      //TURN OFF
      digitalWrite (currentG,LOW);
      digitalWrite (currentR,LOW);
      digitalWrite (changeR,LOW);
      digitalWrite (changeG,LOW); 
      break;
    case '5':
      //TURN ON
      digitalWrite (currentY,HIGH);
      digitalWrite (changeG,HIGH);
      //TURN OFF
      digitalWrite (currentG,LOW);
      digitalWrite (currentR,LOW);
      digitalWrite (changeR,LOW);
      digitalWrite (changeY,LOW);
      break;
    case '6':
      //TURN ON
      digitalWrite (currentY,HIGH);
      digitalWrite (changeR,HIGH);
      //TURN OFF
      digitalWrite (currentG,LOW);
      digitalWrite (currentR,LOW);
      digitalWrite (changeY,LOW);
      digitalWrite (changeG,LOW);
      break;
    case '7':
      //TURN ON
      digitalWrite (currentY,HIGH);
      digitalWrite (changeR,HIGH);
      //TURN OFF
      digitalWrite (currentG,LOW);
      digitalWrite (currentR,LOW);
      digitalWrite (changeY,LOW);
      digitalWrite (changeG,LOW);
      break;
    case '8':
      //TURN ON
      digitalWrite(currentG,HIGH);
      digitalWrite(changeR,HIGH);
      //TURN OFF
      digitalWrite(currentR,LOW);
      digitalWrite(currentY,LOW);
      digitalWrite(changeY,LOW);
      digitalWrite(changeG,LOW);
      break;
    case '9':
      //TURN ON
      digitalWrite(currentG,HIGH);
      digitalWrite(changeR,HIGH);
      //TURN OFF
      digitalWrite(currentR,LOW);
      digitalWrite(currentY,LOW);
      digitalWrite(changeY,LOW);
      digitalWrite(changeG,LOW);
      break;
  }
}

void loop() {
    Serial.println("{\"hpa\": " + (String)bmp.readPressure() + ", \"waterVal\": " + (String)analogRead(A0) + "}");
    pressureValues();
    waterValues();
}
