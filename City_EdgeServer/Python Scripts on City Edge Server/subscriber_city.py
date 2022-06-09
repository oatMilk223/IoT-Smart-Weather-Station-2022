# Name: subscriber_city.py
# Author: Maxwell Hing
# Date: 21 MAY 2022

import paho.mqtt.client as mqtt
import globalvals_city as Global
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/weather_commands/city")

def on_message(client, userdata, msg):
    topic = msg.topic
    data = (msg.payload).decode("utf-8")
    
    print("Recieved Data " + data + " from Topic " + topic + ". ")
    
    input_dict = json.loads(data)
    
    print("Data Parsed. ")
    Global.init_globals()
    for input_key in input_dict:
        for threshold_key in Global.thresholds:
            if (input_key == threshold_key):
                Global.thresholds[threshold_key] = input_dict[input_key]
                print("Threshold " + threshold_key + " set to " + str(Global.thresholds[threshold_key]) + ". ")
     
    
def listen_for_master():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("10.0.2.5", 1883, 60)

    client.loop_forever()

#print(globalvals.TempVal)




