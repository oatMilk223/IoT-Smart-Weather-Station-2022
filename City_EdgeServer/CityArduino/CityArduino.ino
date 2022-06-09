//////////////////////////////////////////////////////////////////////
//////////////////////// IMPORTS AND CONSTANTS ///////////////////////
//////////////////////////////////////////////////////////////////////
char conditionalData;

#include "DHT.h"
//Temperature and Humidity Pins
#define DHTPIN 11
#define DHTTYPE DHT11
//Rain pins
#define rainSensorPower 13
#define rainSensorPin 2



DHT dht(DHTPIN, DHTTYPE);

int buzzer = 4;

int greenLed = 8;
int redLed = 7;
int yellowLed = 6;
int blueLed = 5;

//////////////////////////////////////////////////////////////////////
////////////////////////////// SETUP /////////////////////////////////
//////////////////////////////////////////////////////////////////////

void setup() {
	pinMode(rainSensorPower, OUTPUT);
	digitalWrite(rainSensorPower, LOW);

  dht.begin();

  pinMode(buzzer,OUTPUT);

  pinMode(greenLed, OUTPUT);
  pinMode(redLed, OUTPUT);
  pinMode(yellowLed, OUTPUT);
  pinMode(blueLed, OUTPUT);

  digitalWrite(greenLed, HIGH);
  digitalWrite(redLed, LOW);
  digitalWrite(yellowLed, LOW);
  digitalWrite(blueLed, LOW);

	Serial.begin(9600);
}

//////////////////////////////////////////////////////////////////////
/////////////////////////// FUNCTIONS ////////////////////////////////
//////////////////////////////////////////////////////////////////////

//  This function returns the sensor output for Rain Sensor
int readRainSensor() {
	digitalWrite(rainSensorPower, HIGH);	// Turn the sensor ON
	delay(10);							// Allow power to settle
	int rainVal = digitalRead(rainSensorPin);	// Read the sensor output
	digitalWrite(rainSensorPower, LOW);		// Turn the sensor OFF
	return rainVal;							// Return the value
}

void tempLED(char conditionalData){
  
  switch (conditionalData) {
    case '1':
      digitalWrite(redLed, HIGH);
      digitalWrite(buzzer, HIGH);
      digitalWrite(greenLed, LOW);
      break;
    case '4':
      digitalWrite(redLed, LOW);
      digitalWrite(buzzer, LOW);
    break;
  }
}

void humidLED(char conditionalData){
 
  switch (conditionalData){
    case '2':
      digitalWrite(yellowLed, HIGH);
      digitalWrite(greenLed, LOW);
      break;
    case '5':
      digitalWrite(yellowLed, LOW);
    break;

    }
}

void rainLED(char conditionalData) {
  
  switch (conditionalData) {
    case '3':
      digitalWrite(blueLed, HIGH);
      digitalWrite(greenLed, LOW);
      break;
    case '6':
      digitalWrite(blueLed, LOW);
    break;
  }
}

void shesAllGood(char conditionalData) {
  if (conditionalData == '7') {
    digitalWrite(greenLed, HIGH);
  }
}

//////////////////////////////////////////////////////////////////////
////////////////////////////// LOOP //////////////////////////////////
//////////////////////////////////////////////////////////////////////

void loop() {
 if (Serial.available()){
    conditionalData = Serial.read();
  }
  //conditionalData = Serial.read();
  //Read Rain Sensor Value
	int rainVal = readRainSensor();
	//Start temperature check  
  float h = dht.readHumidity();
  float t = dht.readTemperature(); //As Celcius

  tempLED(conditionalData);
  humidLED(conditionalData);
  rainLED(conditionalData);
  shesAllGood(conditionalData);
  

  Serial.println("{\"Humidity\":"  + (String)h + ",\"Temperature\":" + (String)t + ",\"rain\":" + (String)rainVal + "}");

}
