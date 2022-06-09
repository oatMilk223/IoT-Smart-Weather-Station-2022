# name: MQTT_CORE_CITY.py
# auth: Mafaz Abrar Jan Chowdhury
# date: 16 MAY 2022
# desc: MQTT to CITY DB - python script for Assignment 3

######################################################################
################ IMPORTS AND CONSTANTS ###############################
######################################################################

import paho.mqtt.client as mqttClient
import paho.mqtt.publish as mqttPublish
import pymysql
import json
import GLOBAL_VARIABLES as Global

SENSOR_DATA = {
    "Temperature": {"token": "TEMPERATURE1", "value": "default temp"},
    "Humidity": {"token": "HUMIDITY1", "value": "default humd"},
    "rain": {"token": "RAIN1", "value": "default rain"}
    }

#######################################################################
############### FUNCTIONS #############################################
#######################################################################

def create_sql_table(db_connection):
    
    # Test if table exists
    # Create if not found
    with db_connection:
        with db_connection.cursor() as cursor:
            
            # First, test if table exists
            sql = "SHOW TABLES LIKE 'weather_data_city';" 
            cursor.execute(sql)
            
            result = cursor.fetchone()
            
            # If table does not exist, create table
            if (result is None):
                sql = """CREATE TABLE weather_data_city(
                            data_id INT NOT NULL AUTO_INCREMENT,
                            date DATE NOT NULL,
                            time TIME NOT NULL,
                            temperature FLOAT NOT NULL,
                            humidity FLOAT NOT NULL,
                            rain FLOAT NOT NULL,
                            PRIMARY KEY(data_id)
                        );"""
                
                cursor.execute(sql)
                db_connection.commit()
                
def load_data_from_data_dictionary(data_dictionary):
    
    for senders_key in data_dictionary:
        for receivers_key in SENSOR_DATA:        
            
            if (senders_key == receivers_key):
                SENSOR_DATA[receivers_key]["value"] = int(data_dictionary[senders_key])
                
                
def record_data_in_db(db_connection):
    
    with db_connection:
        with db_connection.cursor() as cursor:
            
            # Add the data into the table, depending on whether the motion
            # was authorized or not
            sql = """INSERT INTO weather_data_city(date, time, temperature, humidity, rain) VALUES (
                        CURDATE(), CURTIME(), '%s', '%s', '%s');""" % (SENSOR_DATA["Temperature"]["value"], SENSOR_DATA["Humidity"]["value"], SENSOR_DATA["rain"]["value"])
            
            cursor.execute(sql)
            db_connection.commit()
            
def send_data_to_thinsgboard():
    
    topic = "v1/devices/me/telemetry"
    qos = 1
    
    for key in SENSOR_DATA:
        
        payload = {key: SENSOR_DATA[key]["value"]}
        auth = {'username': SENSOR_DATA[key]["token"]}
        
        try:
            mqttPublish.single(topic, payload = json.dumps(payload), qos = qos, hostname = Global.THINGSBOARD_HOST_IP, port = Global.THINGSBOARD_HOST_PORT, auth = auth)
        except:
            print("Thingsboard Socket Timeout")
        
# The CALLBACK when a CONACK message is received from the MQTT broker
def mqtt_on_connect(client, userdata, flags, rc):
    
    print("Connected with result code: " + str(rc))
    
    # If we get disconnected, and then we reconnect,
    # we will also be subscribed to the topic specified
    # on reconnect
    client.subscribe("/weather_data/city")
    
    print("Subscribed to topic /weather_data/city. ")
    
# The CALLBACK when a PUBLISH message is received from a client
def mqtt_on_message(client, userdata, msg):
    
    topic = msg.topic
    json_string = (msg.payload).decode("utf-8")
    
    print("Received data: " + json_string + " From Topic: " + topic)
    
    # Parse the data
    data_dictionary = json.loads(json_string)
    
    print("Data parsed. ")
    
    # Load the data into constants
    load_data_from_data_dictionary(data_dictionary)
    
    print("Data loaded. ")
    
    # Set up MySQL Connection
    db_connection = pymysql.connect(host = Global.DB_HOST, user = Global.DB_USER, db = Global.DB_NAME)
    
    # Create Table if not exists
    create_sql_table(db_connection)
    
    # Record data in MySQL
    record_data_in_db(db_connection)
    
    print("Data sent to DB. ")
    
    # Send Data to Thingsboard
    send_data_to_thinsgboard()
    
    print("Data sent to ThingsBoard host " + Global.THINGSBOARD_HOST_IP + " on port " + str(Global.THINGSBOARD_HOST_PORT) + ". ")

def setup_mqtt(client):
    
    # These are callbacks, note that we do not
    # call the functions with (), we simply 
    # attach them to client
    client.on_connect = mqtt_on_connect
    client.on_message = mqtt_on_message
    



#####################################################################
################ MAIN FUNCTION ######################################
#####################################################################

def mqtt_core_city():
    
    client = mqttClient.Client()
    
    # Setup the MQTT Client to subscribe to topic "/weather_data/city"
    setup_mqtt(client)

    # Connect this client to the MQTT Broker (in this case,
    # the MQTT Broker is itself)
    client.connect(Global.MQTT_BROKER_IP, Global.MQTT_BROKER_PORT, 60)

    # The following is a blocking call that processes network traffic,
    # dispatches callbacks and handles reconnect

    # Other loop*() functions are available that give threaded and manual
    # interfaces

    client.loop_forever()
    

