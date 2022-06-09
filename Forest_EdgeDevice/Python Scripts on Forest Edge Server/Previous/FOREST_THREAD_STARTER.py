# name: FOREST.py
# auth: Brooke Johnson
# date: -
# desc: Starts Threads

#####################################################################
################### IMPORTS AND CONSTANTS ###########################
#####################################################################

import FOREST_DISCORD_SUBSCRIBER
import FOREST_MQTT_PUBLISHER

import FOREST_GLOBAL_VARIABLES as Global

import threading


#####################################################################
####################### MAIN FUNCTION ###############################
#####################################################################


def start_threads():
    
    # Initialize global variables
    Global.init_globals()
    
    # Create threads
    thread1 = threading.Thread(target = FOREST_DISCORD_SUBSCRIBER.listen_for_commands_from_master)
    thread2 = threading.Thread(target = FOREST_MQTT_PUBLISHER.push_data_to_master)
    
    # Start threads
    thread1.start()
    thread2.start()
    
if __name__ == "__main__":
    start_threads()
    