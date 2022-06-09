import publisher_city
import globalvals_city as Global
import subscriber_city
import threading


def start_threads():
    thread01 = threading.Thread(target = subscriber_city.listen_for_master)
    thread02 = threading.Thread(target = publisher_city.send_data_to_master)
    
    thread01.start()
    thread02.start()
    
if __name__ == "__main__":
    Global.init_globals()
    start_threads()
    
    

    