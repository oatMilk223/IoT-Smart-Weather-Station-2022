import paho.mqtt.client as mqtt
import json
import Global_Vals_Coastal as g

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc) + ". ")
    client.subscribe("/weather_commands/coastal")
    
def on_message(Client, userdata, msg):
    coastalVal = json.loads(msg.payload)
    
    if (coastalVal.get("thresholdWaterValHigh") is not None):
        g.thresholdWaterValHigh = coastalVal["thresholdWaterValHigh"]
    elif(coastalVal.get("thresholdWaterValLow") is not None):
        g.thresholdWaterValLow = coastalVal["thresholdWaterValLow"]
    elif (coastalVal.get("thresholdHpaHigh") is not None):
        g.thresholdHpaHigh = coastalVal["thresholdHpaHigh"]
    elif (coastalVal.get("thresholdHpaLow") is not None):  
        g.thresholdHpaLow = coastalVal["thresholdHpaLow"]
    elif (coastalVal.get("thresholdPrevHpaHigh") is not None):
        g.thresholdPrevHpaHigh = coastalVal["thresholdPrevHpaHigh"]
    elif (coastalVal.get("thresholdPrevHpaLow") is not None):
        g.thresholdPrevHpaLow = coastalVal["thresholdPrevHpaLow"]
    
    #print(g.thresholdWaterVal, g.thresholdHpaHigh, g.thresholdHpaLow, g.thresholdPrevHpaHigh, g.thresholdPrevHpaLow)

def listener():
    client = mqtt.Client()
    client.connect("10.0.2.5", 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()