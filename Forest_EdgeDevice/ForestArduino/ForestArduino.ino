// name: ForestArduino.ino
// auth:
// date:
// desc:

/////////////////////////////////////////////////////////////////////
//////////////// IMPORTS AND CONSTANTS //////////////////////////////
/////////////////////////////////////////////////////////////////////
// python compatible stuff
char conditionalData;

// DHT Sensor library //
#include "dht.h"

// DHT Sensor Pin
#define dhtPin A0

// Needed for DHT processing
dht DHT;

// Smoke Sensor Pin
#define smokeSensor A5

// LED Pins for Humidity
int humidityGreen= 4;
int humidityYellow = 3;
int humidityRed = 2;

// LED Pins for Temperature
int tempHigh = 6;
int tempLow = 5;
//

// Buzzer
#define buzzerPin 9

/////////////////////////////////////////////////////////////////////
////////////////////////// SETUP ////////////////////////////////////
/////////////////////////////////////////////////////////////////////

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  // Set Humidity LED Pins to OUTPUT mode
  pinMode(humidityGreen, OUTPUT);
  pinMode(humidityYellow, OUTPUT);
  pinMode(humidityRed, OUTPUT);

  // Set Temperature LED Pins to OUTPUT mode
  pinMode(tempHigh, OUTPUT);
  pinMode(tempLow, OUTPUT);

  // Set Buzzer Pin to OUTPUT mode
  pinMode(buzzerPin, OUTPUT);

  // Set Gas/Smoke Sensor Pin to INPUT mode
  pinMode(smokeSensor, INPUT);
}


/////////////////////////////////////////////////////////////////////
/////////////////////////// FUNCTIONS ///////////////////////////////
/////////////////////////////////////////////////////////////////////

// Reads Temperature from DHT sensor
int tempRead(){
  int tempVal = DHT.temperature;
  return tempVal;
}

// Reads Humidity from DHT sensor
int humidityRead(){
  int humidityVal = DHT.humidity;
  return humidityVal;
}

// Reads Gas from Gas Sensor
int gasRead(){
  int gasVal = analogRead(smokeSensor);
  return gasVal;
}

//////////////////////////////////////////////////////////////
////////////////// ACTUATORS /////////////////////////////////
//////////////////////////////////////////////////////////////

// HUMIDITY CHECK W LEDS AND DHT SENSOR VALUE
//checks humidity levels from humidityRead() and triggers appropriate led on (turning others off)
void humidityLED(char conditionalData){
  // high = H, medium = M, def(low)
  switch (conditionalData){
    case 'H':
      // High Humidity
      digitalWrite(humidityGreen, HIGH);
      digitalWrite(humidityYellow, LOW);
      digitalWrite(humidityRed, LOW);

      break;
    case 'M':
      // medium Humidity
      digitalWrite(humidityGreen, LOW);
      digitalWrite(humidityYellow, HIGH);
      digitalWrite(humidityRed, LOW);

      break;
    case 'L':
      // low Humidity
      digitalWrite(humidityGreen, LOW);
      digitalWrite(humidityYellow, LOW);
      digitalWrite(humidityRed, HIGH);

      break;
  }
}


// TEMP CHECK W LEDS AND DHT SENSOR VALUE - change vars
// checks temp levels from tempRead() and triggers appropriate led on (turning others off)
void tempLED(char conditionalData){
  // 0 = high temp, 1 = low temp, else/def = reg (no action)
  switch (conditionalData){
    case '0':
      // High Temperature 
      digitalWrite(tempLow, LOW);
      digitalWrite(tempHigh, HIGH);

      break;
    case '1':
      // Low Temperature
      digitalWrite(tempHigh, LOW);
      digitalWrite(tempLow, HIGH);

      break;
    case '2':
      // Regular Temperature (No LED Warnings)
      digitalWrite(tempHigh, LOW);
      digitalWrite(tempLow, LOW);

      break;
  }
}

void gasBuzz(char conditionalData){ 
  switch (conditionalData){
    // gas = a, no gas = def
    case 'a':
      // gas detected
      tone(buzzerPin, 1000, 500);
      break;
    case 'b':
       // no gas, no buzzer
       tone(buzzerPin, 1, 1);
       break;
  }
}


/////////////////////////////////////////////////////////////////////
/////////////////////////// LOOP ////////////////////////////////////
/////////////////////////////////////////////////////////////////////

void loop() {
   if (Serial.available()){
    conditionalData = Serial.read();
  }

  
  
  // put your main code here, to run repeatedly:

  DHT.read11(dhtPin);
  
  // Read Sensor values
  int humidityVal = humidityRead();
  int tempVal = tempRead();
  int gasVal = gasRead();

  // Apply Conditional Logic
  
  // Humidity Conditional Logic
  humidityLED(conditionalData);
  
  // Temperature Conditional Logic
  tempLED(conditionalData);
  
  // Gas Conditional logic
  gasBuzz(conditionalData);
  
  // Serial Communication
  Serial.println("{\"temperature\": " + (String)tempVal + ", \"humidity\": " + (String)humidityVal + ", \"gasValue\": " + (String)gasVal + "}");
}
