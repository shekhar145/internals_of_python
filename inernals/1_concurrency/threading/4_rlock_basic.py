"""
A reentrant lock is a synchronization primitive that may be acquired multiple times by the same thread. 
Internally, it uses the concepts of “owning thread” and “recursion level” in addition to the locked/unlocked state used by primitive locks. 
In the locked state, some thread owns the lock; in the unlocked state, no thread owns it.


RLock's acquire()/release() call pairs can be nested
Only the final release resets the lock to an unlocked state and allows another thread blocked in acquire() to proceed

acquire()/release() must be used in pairs: each acquire must have a release in the thread that has acquired the lock. Failing to call release as many times the lock has been acquired can lead to deadlock.

How RLock works:-
1. A Counter: This keeps track of how many times the lock has been acquired by the current thread
2. Owner: this stores the identity of the thread that are currently holds the lock
3. When an thread calls the acquire(), Rlock check it's owner
- If the lock is unlocked, the calling thread tbecomes the new owner, and the counter is set to 1.
- If the lock is already owned by same thread, the counter is simply incremented. The thread does not block.
- If the lock is owneed by different thread, the calling thread blocks until the lock is fully released.


Primary Purpose:-
- Primary purpose is to prevent self-deadlock. It occur when a thread which already holds a lock tries to acquire it again
(Standard Lock will block it indefinitely)

"""

# Problem with Lock, infinite blocking

import threading
import time

lock = threading.Lock()

def outer_function():
    print('Outer function tries to acquire lock')
    with lock:
        print('Outer func has acquired lock')
        inner_function()

def inner_function():
    print('Inner function is trying to acquire lock')
    with lock:
        print('Inner function acquired lock')

# thread = threading.Thread(target=outer_function)
# thread.start()
# thread.join()
# It's self Deadlock


# Solution

rlock = threading.RLock()

def outer_function_r():
    print('Outer function tries to acquire lock')
    with rlock:
        print('Outer func has acquired lock')
        inner_function()

def inner_function_r():
    print('Inner function is trying to acquire lock')
    with rlock:
        print('Inner function acquired lock')

thread = threading.Thread(target=outer_function_r)
thread.start()
thread.join()