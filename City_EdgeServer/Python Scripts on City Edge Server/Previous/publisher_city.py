# Name: publisher_city.py
# Author: Maxwell Hing
# Date: 21 MAY 2022

import serial
import paho.mqtt.publish as publish
import globalvals_city as Global
import json
import time
arduinoSer = serial.Serial('/dev/ttyS3', 9600)

def apply_conditional_logic(arduino, sensor_data_json_string):
    sensor_data = json.loads(sensor_data_json_string)
    arduinoSer.reset_input_buffer()
    
    if (sensor_data["temperature"] > Global.thresholds["temperature"]):
        arduinoSer.write(str.encode("1"))        
        print ("WARNING: Temperature is currently above comfortable levels. ")
    elif (sensor_data["temperature"] <= Global.thresholds["temperature"]):
        arduinoSer.write(str.encode("4"))
            
    if (sensor_data["humidity"] > Global.thresholds["humidity"]):
        arduinoSer.write(str.encode("2"))       
        print ("Humidity is currently above a comfortable level. ")
    elif (sensor_data["humidity"] <= Global.thresholds["humidity"]):
        arduinoSer.write(str.encode("5"))
        
    if (sensor_data["rain"] == 1):
        arduinoSer.write(str.encode("3"))
        print("It is currently raining in the city. ")
    elif (sensor_data["rain"] == 0):
        arduinoSer.write(str.encode("6"))
        
    if (sensor_data["temperature"] <= Global.thresholds["temperature"] && sensor_data["humidity"] <= Global.thresholds["humidity"] && sensor_data["rain"] == 0):
        arduinoSer.write(str.encode("7"))
        
        
def send_data_to_master():
    while True:
        json_data = arduinoSer.readline().decode("utf-8")
        publish.single("weather_data/city", json_data, hostname="192.168.56.102")
        print(Global.thresholds["temperature"])
        