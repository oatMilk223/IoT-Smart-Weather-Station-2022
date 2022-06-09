import serial
import Global_Vals_Coastal as g
import requests
import json
import paho.mqtt.publish as publish
import time

line = ""
ser = serial.Serial('/dev/ttyS0', 9600)

def get_change():
    try:
        response = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=-37.8136&lon=144.946457&appid=fda662f1f6b96db6081f83075423ecc2')
        jsonResponse = response.json()
        return jsonResponse["hourly"][0]["pressure"]
    except:
        return 1019

def pressure_values(serialDict):
    
    serialDict = json.loads(serialDict)
    pressureVal = serialDict["hpa"]
    
    #convert to hpa val
    hpa = pressureVal / 100
    previousHpa = get_change()
    
    if hpa < g.thresholdHpaLow and previousHpa >= g.thresholdPrevHpaHigh:
        #current weather = stormy
        #change = clearing
        ser.write(str.encode("1"))
    elif hpa < g.thresholdHpaLow and previousHpa < g.thresholdPrevHpaHigh and g.previousHpa > g.thresholdPrevHpaLow:
        #current weather = windy or stormy
        #change = none
        ser.write(str.encode("2"))
    elif hpa < g.thresholdHpaLow and previousHpa < -g.thresholdPrevHpaLow:
        #current weather = windy or stormy
        #change = worsening
        ser.write(str.encode("3"))
    elif hpa > g.thresholdHpaLow and hpa < g.thresholdHpaHigh and previousHpa >= g.thresholdPrevHpaLow and previousHpa <= g.thresholdPrevHpaLow:
        #current weather = fair
        #change = none
        ser.write(str.encode("4"))
    elif hpa > g.thresholdHpaLow and hpa < g.thresholdHpaHigh and previousHpa > g.thresholdPrevHpaLow:
        #current weather = fair
        #chnage = clearing
        ser.write(str.encode("5"))
    elif hpa > g.thresholdHpaLow and hpa < g.thresholdHpaHigh and previousHpa <= g.thresholdPrevHpaLow:
        #current weather = fair
        #chnage = clearing
        ser.write(str.encode("6"))
    elif hpa > g.thresholdHpaHigh and previousHpa >= g.thresholdPrevHpaHigh:
        #curr weather = dry
        #change = none
        ser.write(str.encode("7"))
    elif hpa > g.thresholdHpaHigh and previousHpa < g.thresholdPrevHpaHigh and previousHpa > g.thresholdPrevHpaLow:
        #curr weather = dry
        #change = cooling
        ser.write(str.encode("8"))
    elif hpa > g.thresholdHpaHigh and previousHpa < g.thresholdPrevHpaLow:
        #curr weather = dry
        #change = cooling rapidly
        ser.write(str.encode("9"))

def water_values(serialDict):
    serialDict = json.loads(serialDict)
    waterVal = serialDict["waterVal"]
    
    if waterVal > g.thresholdWaterValHigh:
        ser.write(str.encode("h"))
    elif waterVal < g.thresholdWaterValHigh and waterVal > g.thresholdWaterValLow:
        ser.write(str.encode("m"))
    else:
        ser.write(str.encode("l"))


def publisher():
    while True:
        try:
    
            serialDict = ser.readline().decode('utf-8')
            ser.reset_input_buffer()
          
            print("Received Data from Arduino " + serialDict)
            #serialDict = json.loads(serialDict)
            
            #publish.single("/weather_data/coastal", serialDict, hostname="10.0.2.5")
            
            #pressure_values(serialDict["hpa"])
            #water_values(serialDict["waterVal"])
            
            pressure_values(serialDict)
            
            water_values(serialDict)
            
            publish.single("/weather_data/coastal", serialDict, hostname="10.0.2.5")
            
        except:
            print("Error")
            
        
        
        
