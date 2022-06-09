# name: global_variables.py
# auth: Mafaz Abrar Jan Chowdhury
# date: 18 MAY 2022
# desc: Global Variables and Constants for Group Assignment

######################################################################
################ IMPORTS AND CONSTANTS ###############################
######################################################################

DB_HOST = "localhost"
DB_USER = "pi"
DB_NAME = "weather_db"

THINGSBOARD_HOST_IP = "10.1.40.67"
THINGSBOARD_HOST_PORT = 1883

MQTT_BROKER_IP = "10.0.2.5"
MQTT_BROKER_PORT = 1883


#######################################################################
############### FUNCTIONS #############################################
#######################################################################

def init_globals():
    # Change names
    # For City, these would be: temperature, humidity
    # Refer to the Standards for each site on Discord
    global thresholds
    global real_data
    
    thresholds = {
        "earthquakeSeverityThreshold": 50
        }
    
    real_data = False
