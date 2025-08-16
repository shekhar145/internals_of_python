"""
This is the standard pattern for using locks in Python as it provides a clean, readable, and robust way to manage synchronization.

"""

import threading

count = 0
count_lock = threading.Lock()

def inc_counter():
    global count
    for _ in range(100000):
        with count_lock:
            count += 1

thread1 = threading.Thread(target=inc_counter)
thread2 = threading.Thread(target=inc_counter)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print(f"Final counter value: {count}")


"""
Important Concepts
Deadlock: This occurs when two or more threads are blocked forever, waiting for each other to release a lock. For example, Thread A holds Lock 1 and waits for Lock 2, while Thread B holds Lock 2 and waits for Lock 1. Neither can proceed. Proper lock ordering and resource management are key to preventing deadlocks.

Starvation: This is a situation where a thread repeatedly loses the race to acquire a lock, even though it's available. It can get "stuck" and never make progress. Python's thread scheduler tries to be fair, but this can still be a concern in certain designs.

Global Interpreter Lock (GIL): In CPython, the default Python interpreter, the GIL ensures that only one thread can execute Python bytecode at a time. While this simplifies some memory management, it means threads are still serialized. Locks are still necessary because they protect against issues within Python code itself, such as data corruption from interleaved operations.

"""