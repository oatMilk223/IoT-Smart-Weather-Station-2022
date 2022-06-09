# name: FOREST.py
# auth: Brooke Johnson
# date: -
# desc: Subscribes to Discord Commands, sets Global Variables

#####################################################################
################### IMPORTS AND CONSTANTS ###########################
#####################################################################

import paho.mqtt.client as mqttClient

import json

import FOREST_GLOBAL_VARIABLES as Global


#####################################################################
########################### FUNCTIONS ###############################
#####################################################################

# On Connect Callback
def on_connect(client, userdata, flags, rc):
    
    print("Connected with result code " + str(rc) + ". ")
    
    # Change to relevant topic
    client.subscribe("/weather_commands/forest")

# On Message Callback
def on_message(client, userdata, msg):
    
    topic = msg.topic
    data = (msg.payload).decode("utf-8")
    
    print("Received Data " + data + " from Topic " + topic + ". :)")
    
    # Dictionary of input values
    # Expected format: {"temperature":25} OR {"humidity":36}
    input_dict = json.loads(data)
    
    print("Data parsed. ")
    
    # Iterate through both Dictionaries
    for input_key in input_dict:
        for threshold_key in Global.thresholds:
            
            # For the matching threshold
            if (input_key == threshold_key):
                
                # Set the threshold to the input value
                Global.thresholds[threshold_key] = input_dict[input_key]
                print("Threshold " + threshold_key + " set to " + str(Global.thresholds[threshold_key]) + ". ")    


#####################################################################
####################### MAIN FUNCTION ###############################
#####################################################################
    
def listen_for_commands_from_master():
    
    # Create Client Object
    client = mqttClient.Client()
    
    # Attach Callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    
    # Connect to MQTT Broker
    # The IP here may change
    client.connect("10.0.2.5", 1883, 60)
    
    client.loop_forever()
