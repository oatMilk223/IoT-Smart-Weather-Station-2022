# name: FOREST.py
# auth: Brooke Johnson
# date: -
# desc: Retrieves data from Arduino, checks with Conditional Logic, sends up to Master

#####################################################################
################### IMPORTS AND CONSTANTS ###########################
#####################################################################

import serial
import paho.mqtt.publish as Publish
import FOREST_GLOBAL_VARIABLES as Global
import json
import time

#####################################################################
########################### FUNCTIONS ###############################
#####################################################################

def apply_conditional_logic(arduino, sensor_data_json_string):
    
    # Load data from string to dictionary
    sensor_data = json.loads(sensor_data_json_string)
    
    # If the condition matches, send the appropriate code
    
    # If temperature greater than threshold
    if (sensor_data["temperature"] >= Global.thresholds["temperatureHigh"]):
        #arduino.write("0")
        print("Temperature is High. ")
        
    if (sensor_data["temperature"] <= Global.thresholds["temperatureLow"]):
        #arduino.write("1")
        print("Temperature is Low. ")
        
    # If humidity is less than threshold
    if (sensor_data["humidity"] >= Global.thresholds["humidityHigh"]):
        #arduino.write("H")
        print("Humidity is High. ")
        
    if (sensor_data["humidity"] < Global.thresholds["humidityHigh"] && sensor_data["humidity"] > Global.thresholds["humidityLow"]):
        #arduino.write("M")
        print("Some humidity. ")
        
    if (sensor_data["gasValue"] >= Global.thresholds["gasDetected"]):
        #arduino.write("a")
        print("Gas detected, there may be a fire nearby. ")
   


#####################################################################
####################### MAIN FUNCTION ###############################
#####################################################################

def push_data_to_master():
    
    # Create the Serial object
    #arduino = serial.Serial("/dev/ttyS0",9600)
    arduino = "Hello there"
    
    while True:
        
        time.sleep(5)
        
        # Read in Serial data
        # This will be a JSON string
        #sensor_data_json_string = arduino.readline()
        sensor_data_json_string  = "{\"temperature\":80,\"humidity\":27, \"gasValue\":1}"
        # not rly used ^^^^^
        
        print("Data read from Sensors: " + sensor_data_json_string  + ". ")
        
        # Apply the Conditional Logic
        apply_conditional_logic(arduino, sensor_data_json_string)
        
        # Push data to Master
        # Change topic to Relevant topic
        # May need to change hostname
        Publish.single("/weather_data/forest", sensor_data_json_string, hostname = "10.0.2.5")
        
        
        