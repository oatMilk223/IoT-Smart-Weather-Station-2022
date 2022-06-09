import paho.mqtt.client as mqtt
import json
import Global_Vals_Coastal as g

def on_connect(client, userdata, flags, rc):
    print(str(rc))
    client.subscribe("/weather_command/coastal")
    
def on_message(Client, userdata, msg):
    coastalVal = json.loads(msg.payload)
    g.thresholdWaterVal = coastalVal["thresholdWaterVal"]
    g.thresholdHpaHigh = coastalVal["thresholdHpaHigh"]
    g.thresholdHpaLow = coastalVal["thresholdHpaLow"]
    g.thresholdPrevHpaHigh = coastalVal["thresholdPrevHpaHigh"]
    g.thresholdPrevHpaLow = coastalVal["thresholdPrevHpaLow"]
    
    print(g.thresholdWaterVal, g.thresholdHpaHigh, g.thresholdHpaLow, g.thresholdPrevHpaHigh, g.thresholdPrevHpaLow)

def listener():
    client = mqtt.Client()
    client.connect("10.0.2.5", 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()