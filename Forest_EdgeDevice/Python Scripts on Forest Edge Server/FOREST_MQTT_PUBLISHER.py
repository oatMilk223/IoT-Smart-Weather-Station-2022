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
        arduino.write(str.encode("0"))
        print("Temperature is High. ")
        
    elif (sensor_data["temperature"] <= Global.thresholds["temperatureLow"]):
        arduino.write(str.encode("1"))
        print("Temperature is Low. ")
    
    else:
        arduino.write(str.encode("2"))
        
    # If humidity is less than threshold
    if (sensor_data["humidity"] >= Global.thresholds["humidityHigh"]):
        arduino.write(str.encode("H"))
        print("Humidity is High. ")
        
    elif (sensor_data["humidity"] < Global.thresholds["humidityHigh"] and sensor_data["humidity"] > Global.thresholds["humidityLow"]):
        arduino.write(str.encode("M"))
        print("Some humidity. ")
    
    else:
        arduino.write(str.encode("L"))
        print("Low humidity. ")
        
    if (sensor_data["gasValue"] >= Global.thresholds["gasDetected"]):
        arduino.write(str.encode("a"))
        print("Gas detected, there may be a fire nearby. ")
    
    else:
        arduino.write(str.encode("b"))
        print("No Gas. ")
   


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
            
            print("Data read from Sensors: " + sensor_data_json_string  + ". ")
            
            # Apply the Conditional Logic
            apply_conditional_logic(arduino, sensor_data_json_string)
            
            # Push data to Master
            # Change topic to Relevant topic
            # May need to change hostname
            Publish.single("/weather_data/forest", sensor_data_json_string, hostname = "10.0.2.5")
        
        except:
            print("Error")
        
        