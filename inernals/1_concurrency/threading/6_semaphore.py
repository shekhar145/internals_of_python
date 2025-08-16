"""
A Semaphore is a synchronization primitive used in concurrent programming to control access to a shared resource with a limited number of "slots" or "units." 🚦 Unlike a lock, which can be acquired by only one thread at a time, a semaphore can be acquired by a certain number of threads simultaneously.

It's essentially a counter. When a thread acquires a semaphore, the counter decreases. When a thread releases it, the counter increases.

Key Methods
Semaphore(value): You initialize a semaphore with an integer value, which represents the number of available resources.

acquire(): A thread calls this method to gain access.

If the semaphore's counter is greater than zero, the thread acquires the semaphore, and the counter is decremented by one. The thread continues its execution without blocking.

If the counter is zero, the thread is put into a waiting (blocked) state until another thread releases the semaphore.

release(): A thread calls this method after it has finished using the resource. This increments the semaphore's counter by one, potentially waking up one of the waiting threads.

Analogy: A Limited Parking Lot 🅿️
Think of a semaphore as a parking lot with a fixed number of spaces.

Semaphore(5): This is a parking lot with 5 empty spaces.

acquire(): A car (thread) drives into the lot. If there's a space, it takes one, and the number of empty spaces decreases by one. If the lot is full, the car has to wait outside.

release(): A car leaves the lot, freeing up a space. The number of empty spaces increases, and a waiting car can now enter.

The semaphore ensures that no more than 5 cars can be in the lot at the same time. This is a classic example of a Bounded Resource Pool, a common application for semaphores.


"""


import threading
import time
import random

# A semaphore to limit concurrent database connections to 3
DB_CONNECTIONS_LIMIT = 3
connection_semaphore = threading.Semaphore(DB_CONNECTIONS_LIMIT)

def get_db_connection(thread_name):
    """Simulates a thread acquiring a limited database connection."""
    print(f"Thread {thread_name}: Waiting to acquire a connection...")
    connection_semaphore.acquire()  # Blocks if no connections are available
    
    print(f"Thread {thread_name}: Acquired a connection! Doing some work...")
    # Simulate a database query
    time.sleep(random.uniform(1, 3))
    
    print(f"Thread {thread_name}: Finished work. Releasing the connection.")
    connection_semaphore.release()  # Frees up a slot for another thread

def run_threads():
    # Create 10 threads to simulate a high load
    threads = []
    for i in range(10):
        thread = threading.Thread(target=get_db_connection, args=(f"T-{i}",))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

# best proactice is with
def get_db_connection_with(thread_name):
    """Simulates a thread acquiring a limited database connection."""
    print(f"Thread {thread_name}: Waiting to acquire a connection...")
    
    # Use 'with' to automatically acquire and release the semaphore
    with connection_semaphore:
        print(f"Thread {thread_name}: Acquired a connection! Doing some work...")
        # Simulate a database query
        time.sleep(random.uniform(1, 3))
    
    print(f"Thread {thread_name}: Finished work and released the connection.")

if __name__ == "__main__":
    run_threads()