"""
a Lock is a synchronization primitive used to protect shared resources from being accessed by multiple threads at the same time. 
🔒 It's a fundamental tool for preventing race conditions, which occur when multiple threads try to read or write to the same data simultaneously, leading to unpredictable results.

How a Lock Works
A Lock object has two states: locked and unlocked. It's initially unlocked.

Acquiring a Lock: A thread that wants to access a shared resource must first call the acquire() method on the Lock object.

If the lock is unlocked, the thread acquires it, and the lock's state becomes locked. The thread can now safely access the shared resource.

If the lock is locked by another thread, the calling thread is put into a waiting (blocked) state until the lock is released.

Releasing a Lock: After the thread is done with the shared resource, it must call the release() method to change the lock's state back to unlocked. This signals to waiting threads that the resource is now available.

The crucial part is that only one thread can hold a lock at any given time. This ensures mutual exclusion—only one thread can enter the "critical section" of code where the shared resource is being accessed.
"""
import threading
import time

count_lock = threading.Lock()
count = 0
def inc_counter():
    global count
    for _ in range(100000):
        count_lock.acquire()
        try:
            count += 1
        finally:
            pass
            count_lock.release()
thread1 = threading.Thread(target=inc_counter)
thread2 = threading.Thread(target=inc_counter)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print(f"Final counter value: {count}")

# manually acquire and releasing is error prone