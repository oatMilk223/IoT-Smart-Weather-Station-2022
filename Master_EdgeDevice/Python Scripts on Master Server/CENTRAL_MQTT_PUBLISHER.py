# name: CENTRAL_PUBLISHER_MQTT.py
# auth: Mafaz Abrar Jan Chowdhury
# date: 21 MAY 2022
# desc: Retrieves data from Arduino, checks with Conditional Logic, sends up to Master

#####################################################################
################### IMPORTS AND CONSTANTS ###########################
#####################################################################

import serial
import paho.mqtt.publish as Publish
import GLOBAL_VARIABLES as Global
import json


#####################################################################
########################### FUNCTIONS ###############################
#####################################################################

def apply_conditional_logic(arduino, sensor_data_json_string):
    
    # Load data from string to dictionary
    sensor_data = json.loads(sensor_data_json_string)
    
    # If the condition matches, send the appropriate code
    
    if(sensor_data["earthquake_occurring"] == 1):
        
        Global.real_data = False
        
        # If earthquakeSeverity is greater than threshold
        if (sensor_data["earthquake_severity"] < Global.thresholds["earthquakeSeverityThreshold"]):
            # Send Weak Earthquake Code
            # Ye
            arduino.write(str.encode("0"))
        
        else:
            # Send Strong Earthquake Code
            # Re
            arduino.write(str.encode("1"))
    else:
        
        Global.real_data = True
        # Turn off all LEDs (No Earthquake)
        arduino.write(str.encode("2"))


#####################################################################
####################### MAIN FUNCTION ###############################
#####################################################################

def push_data_to_master():
        
    # Create the Serial object
    arduino = serial.Serial("/dev/ttyS0",9600)
    
    while True:
        
        try:
            # Read in Serial data
            # This will be a JSON string
            sensor_data_json_string = arduino.readline().decode("utf-8")
            arduino.reset_input_buffer()
            
            print("Data read from Sensors: " + sensor_data_json_string)
            
            # Apply the Conditional Logic
            apply_conditional_logic(arduino, sensor_data_json_string)
            
            # Push data to Master
            # Change topic to Relevant topic
            # May need to change hostname
            if (Global.real_data):
                Publish.single("/weather_data/central", sensor_data_json_string, hostname = "10.0.2.5")
        except:
            print("Error")
        
        
        