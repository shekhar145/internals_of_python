"""
A Timer is a subclass of the Thread class and is used for delayed execution. 
It schedules a function to run after a specific amount of time has passed, but it runs that function on a separate thread.

"""
# creation
import threading

def delayed_function():
    print("This function ran after a delay!")

# Create a timer that will run `delayed_function` after 5 seconds
t = threading.Timer(5, delayed_function)

# Start and execution
print("Main thread: Starting the timer...")
t.start()
print("Main thread: The timer is now running in the background.")

# cancellation:- you can cancel it anytime
import time
t_cancellable = threading.Timer(10, delayed_function)
t_cancellable.start()
time.sleep(2)
t_cancellable.cancel()
print("Main thread: Timer was canceled.")




# Retry mechanism

import threading
import time
import random

MAX_RETRIES = 3
retries = 0

def connect_to_server():
    global retries
    print(f"Attempting to connect to server (Retry {retries})...")
    
    # Simulate a connection attempt
    if random.choice([True, False, False]):  # Simulate a 1/3 chance of success
        print("Successfully connected!")
        return True
    else:
        retries += 1
        print("Connection failed.")
        if retries < MAX_RETRIES:
            print("Scheduling a retry in 5 seconds.")
            t = threading.Timer(5, connect_to_server)
            t.start()
        else:
            print("Maximum retries exceeded. Giving up.")
            return False

if __name__ == "__main__":
    connect_to_server()
    # The main thread can continue its work while the Timer is in the background
    print("Main thread is now free to do other tasks.")

