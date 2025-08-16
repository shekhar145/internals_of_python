"""
If you have a global variable, all threads share the same value. 
If one thread changes it, the change is visible to all other threads.
 With a thread-local variable, each thread gets its own private copy. When a thread modifies its copy, it doesn't affect the values in other threads. .

"""
import threading
import time


# each thread will create copy of this variable
my_data = threading.local()
def worker():
    my_data.x = threading.current_thread().name
    print(f"Thread {my_data.x} is starting")
    time.sleep(1)
    print(f"Thread {my_data.x} has finished")

def local_1():

    thread1 = threading.Thread(target=worker,name='Thread-1')
    thread2 = threading.Thread(target=worker,name='Thread-2')

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

print(local_1())
