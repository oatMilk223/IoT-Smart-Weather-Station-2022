# name: 
# auth:
# date:
# desc: The Discord Bot using the Discord API, used to pass commands and view data

###############################################################################
######################## IMPORTS AND CONSTANTS ################################
###############################################################################

# Imports for Discord API #
import discord
from discord.ext import commands
import typing

# Imports for MQTT #
import paho.mqtt.publish as publish

# Imports for SQL Connection and SQL Data Processing #
import GLOBAL_VARIABLES as Global
import pymysql
from datetime import datetime

# Imports for Threading #
import MQTT_CORE_CENTRAL
import MQTT_CORE_CITY
import MQTT_CORE_COASTAL
import MQTT_CORE_FOREST
import threading

# Bot Token for Discord #
TOKEN = 'OTc2MDAxNzMyNjQ1NjE3NzE0.G0_W0x._BWkUeqSIhtwn6IPHvBW1RWIxTQAuDgKnT675c'


###############################################################################
############################## FUNCTIONS ######################################
###############################################################################

# Code to execute a given SQL query and return 
def execute_sql_query(query):
    
    db_connection = pymysql.connect(host = Global.DB_HOST, user = Global.DB_USER, db = Global.DB_NAME)
    
    result = None
    
    with db_connection:
        with db_connection.cursor() as cursor:
            
            # First, test if table exists
            sql = query 
            cursor.execute(sql)
            
            result = cursor.fetchall()
    
    return result


###############################################################################
########################## BOT FUNCTIONS ######################################
###############################################################################

description = """Weather Bot"""
bot = commands.Bot(command_prefix = '?', description = description)

@bot.event
async def on_ready():
    print('Logged in as ')
    print(bot.user.name)
    print(bot.user.id)
    print('-----------')
    
@bot.command()
async def setThreshold(ctx, station_name: str = "", threshold_name: str = "", value: int = -1):
    """For [Arg 1: Station Name], sets [Arg 2: Threshold Name] threshold to [Arg 3: Value]"""
    
    # Check for valid input
    if (station_name == "" or threshold_name == "" or value == -1):
        await ctx.send("""```Please supply all three of the following values:\nThe Weather Station Name,\nthe name for the threshold to be changed,\nand the Value to set the threshold to. ```""")
        return
    
    # Build the MQTT message
    topic = "/weather_commands/{0}".format(station_name)
    message = "{{\"{0}\":{1}}}".format(threshold_name, str(value))
    
    # Send the MQTT message
    publish.single(topic, message, hostname=Global.MQTT_BROKER_IP)
    
    await ctx.send("Set " + threshold_name + " threshold in " + station_name + " to " + str(value) + ". ")
    

@bot.command()
async def viewData(ctx, station_name: typing.Optional[str] = "", column_name: typing.Optional[str] = "", operator: typing.Optional[str] = "", value: typing.Optional[int] = -9999):
    """View Data from [Arg 1: Station Name] [Where [Arg 2: Column] [Arg 3: Operator] [Arg 4: Value]]"""
    
    # Check for valid input
    if (station_name == ""):
        await ctx.send("```Please pass in at least a Weather Station Name. ```")
        return
    
    # Build the SQL Query
    table = "weather_data_" + station_name
    
    sql = "SELECT * FROM {0}".format(table)
    
    if (value != -9999):
        sql += " WHERE {0} {1} {2}".format(column_name, operator, value)
    
    sql += ";"
    
    # Execut the SQL query and store the
    # resulting tuple of tuples
    result = execute_sql_query(sql)
    
    # Check for valid output
    if result is None:
        await ctx.send("Result Set empty. ")
        return
    
    await ctx.send("Results found - Displaying Resultant Data Points. ")
    
    # for each 'row' in the result, send the data  
    for row_number in range(len(result)):
        
        await ctx.send("Data Point Number {0}".format(row_number))
        
        data_point = result[row_number]
        
        date = data_point[1].strftime("%x")
        time = datetime.now() + data_point[2]
        time = time.strftime("%X")
        data_dict = {}
        
        send = "Date: {0}, Time: {1}, ".format(date, time)
        
        if (table == "weather_data_city"):
            data_dict['temp'] = data_point[3]
            data_dict['humd'] = data_point[4]
            data_dict['rain'] = data_point[5]
            
            send += "Temperature: {0}, Humidity: {1}, Rain: {2}".format(data_dict['temp'], data_dict['humd'], data_dict['rain'])
        
        elif (table == "weather_data_coastal"):
            data_dict['airp'] = data_point[3]
            data_dict['wtrl'] = data_point[4]
            
            send += "Air Pressure: {0}, Water Level: {1}".format(data_dict['airp'], data_dict['wtrl'])
        
        elif (table == "weather_data_forest"):
            data_dict['temp'] = data_point[3]
            data_dict['humd'] = data_point[4]
            data_dict['smok'] = data_point[5]
            
            send += "Temperature: {0}, Humidity: {1}, Smoke: {2}".format(data_dict['temp'], data_dict['humd'], data_dict['smok'])
        
        elif (table == "weather_data_central"):
            data_dict['ears'] = data_point[3]
            data_dict['eard'] = data_point[4]
            
            send += "Earthquake Severity: {0}, Earthquake Duration: {1}".format(data_dict['ears'], data_dict['eard'])
        
        await ctx.send(send)
        
    await ctx.send("All Results Displayed. ")
    
    
###############################################################################
############################## THREADING ######################################
###############################################################################

thread1 = threading.Thread(target = MQTT_CORE_CENTRAL.mqtt_core_central)
thread2 = threading.Thread(target = MQTT_CORE_CITY.mqtt_core_city)
thread3 = threading.Thread(target = MQTT_CORE_COASTAL.mqtt_core_coastal)
thread4 = threading.Thread(target = MQTT_CORE_FOREST.mqtt_core_forest)


###############################################################################
############################ MAIN FUNCTION ####################################
###############################################################################

def start_bot_thread():
    bot.run(TOKEN)
    
if __name__ == "__main__":
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    start_bot_thread()
    
