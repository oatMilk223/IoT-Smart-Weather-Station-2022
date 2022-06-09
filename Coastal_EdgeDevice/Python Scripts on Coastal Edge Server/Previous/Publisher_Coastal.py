import serial
import Global_Vals_Coastal as g
import requests
import json
import paho.mqtt.publish as publish
line = ""
ser = serial.Serial('/dev/ttyS0', 9600)

def get_change():
    response = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=-37.8136&lon=144.946457&appid=fda662f1f6b96db6081f83075423ecc2')
    jsonResponse = response.json()
    return jsonResponse["hourly"][0]["pressure"]

def pressure_values(pressureVal):
    #convert to hpa val
    hpa = pressureVal / 100
    previousHpa = get_change()
    
    if hpa < g.thresholdHpaLow and previousHpa >= g.thresholdPrevHpaHigh:
        #current weather = stormy
        #change = clearing
        print(1)
        ser.write(str.encode("1"))
    elif hpa < g.thresholdHpaLow and previousHpa < g.thresholdPrevHpaHigh and g.previousHpa > g.thresholdPrevHpaLow:
        #current weather = windy or stormy
        #change = none
        print(2)
        ser.write(str.encode("2"))
    elif hpa < g.thresholdHpaLow and previousHpa < -g.thresholdPrevHpaLow:
        #current weather = windy or stormy
        #change = worsening
        print(3)
        ser.write(str.encode("3"))
    elif hpa > g.thresholdHpaLow and hpa < g.thresholdHpaHigh and previousHpa >= g.thresholdPrevHpaLow and previousHpa <= g.thresholdPrevHpaLow:
        #current weather = fair
        #change = none
        print(4)
        ser.write(str.encode("4"))
    elif hpa > g.thresholdHpaLow and hpa < g.thresholdHpaHigh and previousHpa > g.thresholdPrevHpaLow:
        #current weather = fair
        #chnage = clearing
        print(5)
        ser.write(str.encode("5"))
    elif hpa > g.thresholdHpaLow and hpa < g.thresholdHpaHigh and previousHpa <= g.thresholdPrevHpaLow:
        #current weather = fair
        #chnage = clearing
        print(6)
        ser.write(str.encode("6"))
    elif hpa > g.thresholdHpaHigh and previousHpa >= g.thresholdPrevHpaHigh:
        #curr weather = dry
        #change = none
        print(7)
        ser.write(str.encode("7"))
    elif hpa > g.thresholdHpaHigh and previousHpa < g.thresholdPrevHpaHigh and previousHpa > g.thresholdPrevHpaLow:
        #curr weather = dry
        #change = cooling
        print(8)
        ser.write(str.encode("8"))
    elif hpa > g.thresholdHpaHigh and previousHpa < g.thresholdPrevHpaLow:
        #curr weather = dry
        #change = cooling rapidly
        print(9)
        ser.write(str.encode("9"))

def water_values(waterVal):
    if waterVal > g.thresholdWaterVal:
        ser.write(str.encode("l"))
    elif waterVal < g.thresholdWaterVal and waterVal > g.thresholdWaterVal:
        ser.write(str.encode("m"))
    else:
        ser.write(str.encode("h"))


def publisher():
    while True:
        serialDict = ser.readline().decode('utf-8')
        publish.single("/weather_data/coastal", serialDict, hostname="10.0.2.15")
        print(serialDict)
        serialDict = json.loads(serialDict)
        pressure_values(serialDict["hpa"])
        water_values(serialDict["waterVal"])
        
        
