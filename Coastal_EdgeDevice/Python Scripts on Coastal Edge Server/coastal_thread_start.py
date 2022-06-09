import Publisher_Coastal
import Subscriber_Coastal
import Global_Vals_Coastal
import threading

def start_threads():
    thread01 = threading.Thread(target = Subscriber_Coastal.listener)
    thread02 = threading.Thread(target = Publisher_Coastal.publisher)
    
    thread01.start()
    thread02.start()
    
if __name__ == "__main__":
    start_threads()