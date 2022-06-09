// name: VibrationSensor
// auth: Mafaz Abrar Jan Chowdhury
// date: 15 MAY 2022
// desc: Vibration Sensor Code


/////////////////////////////////////////////////
//////////// IMPORTS AND CONSTANTS //////////////
/////////////////////////////////////////////////

#define sensorPin A0
#define buzzerPin A5
#define yellowLedPin 5
#define redLedPin 4 

const int BASELINE = 379; 

int earthquakeStartTime = -1;
int earthquakeStopTime = -1;

float earthquakeSeverity = -1;
float earthquakeDuration = -1;

bool earthquakeSeveritySet = false;

bool earthquakeOccurringState = false;

char flag;

/////////////////////////////////////////////////
//////////////////// SETUP //////////////////////
/////////////////////////////////////////////////

void setup() {
  // Only for debugging
  Serial.begin(9600);
  
  pinMode(sensorPin, INPUT);
  pinMode(yellowLedPin, OUTPUT);
  pinMode(redLedPin, OUTPUT);
}

/////////////////////////////////////////////////
///////////////// FUNCTIONS /////////////////////
/////////////////////////////////////////////////

bool checkEarthquakeOccurring() {
  int value = analogRead(sensorPin);
  
  if (value >= BASELINE) {
    return false;
  }

  if (!earthquakeSeveritySet) {
    earthquakeSeverity = value;
  }
  
  return true;
}

void applyFlag(char flag) {
   
  switch (flag) {
    case '0':
      // YELLOW ON, RED OFF 
      // WEAK EARTHQUAKE 
      digitalWrite(yellowLedPin, HIGH);
      digitalWrite(redLedPin, LOW);
      //delay(5000);
      break;
      
    case '1':
      // RED ON, YELLOW OFF
      // BUZZER ON
      // STRONG EARTHQUAKE
      digitalWrite(yellowLedPin, LOW);
      digitalWrite(redLedPin, HIGH);
      tone(buzzerPin, 1000, 500);
      //delay(5000);
      break;
      
    case '2':
      digitalWrite(yellowLedPin, LOW);
      digitalWrite(redLedPin, LOW);
      tone(buzzerPin, 1, 1);
      break;
  }
}

/////////////////////////////////////////////////
//////////////////// LOOP ///////////////////////
/////////////////////////////////////////////////

void loop() {
  /////////////////////////////////////////////////////////////////////////
  ///////////////////////// ACTUATORS /////////////////////////////////////
  /////////////////////////////////////////////////////////////////////////

  if (Serial.available()) {
    flag = Serial.read();
  }

  applyFlag(flag);
  
  /////////////////////////////////////////////////////////////////////////
  ///////////////////////// SENSORS ///////////////////////////////////////
  /////////////////////////////////////////////////////////////////////////
  
  // If the current state is true and the previous state is false
  // We are moving from no Earthquake to Earthquake
  // Record the starting time
  if (checkEarthquakeOccurring() == true && earthquakeOccurringState == false) {
    
    earthquakeOccurringState = true;
    earthquakeDuration = -1;

    earthquakeStartTime = millis();
    earthquakeSeverity = ((379 - earthquakeSeverity) / 379.0) * 100;
    Serial.println("{\"earthquake_occurring\": 1, \"earthquake_severity\": " + (String)earthquakeSeverity + "}");
    
    delay(1000);
    earthquakeSeveritySet = true;
  }
  
  // If the current state is false and the previous state is true
  // We are moving from Earthquake to no Earthquake 
  else if (checkEarthquakeOccurring() == false && earthquakeOccurringState == true) {

    bool stateReallyFalse = true;

    // Ensure state is actually false and not a debounce issue
    for (int i = 0; i < 800; i++) {
      if (checkEarthquakeOccurring() == true) {
        stateReallyFalse = false;
      }
      delay(1);
    }

    if (stateReallyFalse) {
      earthquakeOccurringState = false;
      earthquakeStopTime = millis();

      earthquakeDuration = (earthquakeStopTime - earthquakeStartTime) / 1000.0;
      //Serial.print(" StopTime: " + (String)earthquakeStopTime);
      //Serial.print(" Duration: " + (String)earthquakeDuration);
      //Serial.println(" Severity: " + (String)earthquakeSeverity);

      Serial.println("{\"earthquake_occurring\": 0, \"earthquake_duration\": " + (String)earthquakeDuration + ", \"earthquake_severity\": " + (String)earthquakeSeverity + "}");
      earthquakeSeveritySet = false;
    }
  }
}
