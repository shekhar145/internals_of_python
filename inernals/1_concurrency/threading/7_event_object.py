"""

An Event object is a simple yet powerful synchronization primitive in Python's threading module. It acts as a signaling mechanism that allows one thread to notify other threads about a specific event. 🚩 Its core function is to provide a way for threads to wait for a condition to become true without wasting CPU cycles by busy-waiting.

How It Works
An Event object has a single internal flag that can be in one of two states: True or False.

event.wait(timeout=None): This method blocks a thread until the internal flag is set to True.

If the flag is already True, the method returns immediately.

If the flag is False, the calling thread is put into a waiting state until another thread calls set().

An optional timeout argument can be provided to specify how long to wait before the method returns, even if the flag remains False.

event.set(): This method changes the internal flag to True. This wakes up all threads that are currently blocked on the wait() method. The flag remains True until another thread calls clear()

"""

import threading
import time

# Create a start and a stop event
start_event = threading.Event()
stop_event = threading.Event()

def worker():
    print(f"Worker {threading.current_thread().name} is ready. Waiting for start signal...")
    start_event.wait()  # Block until the start_event flag is True
    print(f"Worker {threading.current_thread().name} has started.")
    
    while not stop_event.is_set():
        # Do some work
        print(f"Worker {threading.current_thread().name} is working...")
        time.sleep(1)

    print(f"Worker {threading.current_thread().name} received stop signal and is shutting down.")

# Main thread
if __name__ == "__main__":
    threads = []
    for i in range(3):
        thread = threading.Thread(target=worker, name=f"Thread-{i}")
        threads.append(thread)
        thread.start()

    print("Main thread: All workers are waiting...")
    time.sleep(2)
    
    print("Main thread: Signaling all workers to start!")
    start_event.set() # Set the flag to True, unblocking all waiting threads
    
    time.sleep(5)
    
    print("Main thread: Signaling all workers to stop!")
    stop_event.set() # Set the flag to True, causing the worker loops to exit
    
    for thread in threads:
        thread.join()
    
    print("Main thread: All workers have finished.")