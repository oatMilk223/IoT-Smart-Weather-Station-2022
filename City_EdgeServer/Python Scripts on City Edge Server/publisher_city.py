# Name: publisher_city.py
# Author: Maxwell Hing
# Date: 21 MAY 2022

import serial
import paho.mqtt.publish as publish
import globalvals_city as Global
import json
import time
arduinoSer = serial.Serial('/dev/ttyS0', 9600)

def apply_conditional_logic(arduino, sensor_data_json_string):
    sensor_data = json.loads(sensor_data_json_string)
    #arduinoSer.reset_input_buffer()
    
    if (sensor_data["Temperature"] > Global.thresholds["temperature"]):
        arduinoSer.write(str.encode("1"))        
        print ("WARNING: Temperature is currently above comfortable levels. ")
    elif (sensor_data["Temperature"] <= Global.thresholds["temperature"]):
        arduinoSer.write(str.encode("4"))
            
    if (sensor_data["Humidity"] > Global.thresholds["humidity"]):
        arduinoSer.write(str.encode("2"))       
        print ("Humidity is currently above a comfortable level. ")
    elif (sensor_data["Humidity"] <= Global.thresholds["humidity"]):
        arduinoSer.write(str.encode("5"))
        
    if (sensor_data["rain"] == 1):
        arduinoSer.write(str.encode("3"))
        print("It is currently raining in the city. ")
    elif (sensor_data["rain"] == 0):
        arduinoSer.write(str.encode("6"))
        print("It is currently NOT raining in the city. ")
    
    if (sensor_data["Temperature"] <= Global.thresholds["temperature"] and sensor_data["Humidity"] <= Global.thresholds["humidity"] and sensor_data["rain"] == 0):
        arduinoSer.write(str.encode("7"))
        print("All good. ")
        
        
def send_data_to_master():
    while True:
        try:
            
            json_data = arduinoSer.readline().decode('utf-8')
            

            
            arduinoSer.reset_input_buffer()
            
            print("Data received from Arduino " + json_data)
            
            apply_conditional_logic(arduinoSer, json_data)
            
            publish.single("/weather_data/city", json_data, hostname="10.0.2.5")
            
            
        
        except:
            print("Error")        


            
       
        