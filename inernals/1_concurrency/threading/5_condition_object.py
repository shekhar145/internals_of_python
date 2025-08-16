"""
Condiiton object in Python threading module is a powerful synchronization primtive that allows threads to wait for specific event to occur. 
It's more advanced tool than a simple Lock or Event because it combines a lock with waiting mechanism

Key Concepts:-
- Associated with lokcs:- it's always tied to a lock, either one you provide or it creates itself. 
This lock is used to protect the shared state that threads are waiting for

- Waiting and Notifying:-
1. wait():- A thread that call wait will atomically release the associated lock and block until it's woken by another thread.
When it wakes up by another thread. When it wakes up, it re-acquire the lock before returning from wait()
2. notify():- A thread that calls notify()  wakes up at most one of the threads that are currently waiting on the condition
3. notify_all():- A thread that calls notify_all() wakes up all of the thread that are waiting on condition

The Shared State: A Condition object is used to synchronize access to a shared resource that has a certain state. Threads waiting on the condition are waiting for that state to change. The associated lock ensures that checking and modifying the state is an atomic operation, preventing race conditions.




Imagine a shared coffee pot with a limited capacity.

The Lock: The coffee pot itself is the shared resource, so we need a lock to prevent two people from pouring at the same time.

The Condition: The Condition is a state-based signal. People who want coffee check if the pot is empty. If it is, they can't pour, so they "wait" for the pot to be refilled.

The wait() Method: A person (thread) who sees an empty pot would say, "I'll wait until there's coffee," and then release their hold on the pot (the lock).

The notify_all() Method: When the pot is refilled, the person who did it would shout, "Coffee's ready!" to wake up everyone who was waiting.

"""

import threading
import time
import collections

queue = collections.deque(maxlen=10)
condition = threading.Condition()

def producer():
    for i in range(20):
        with condition:
            if len(queue) == 10:
                print('Producer queue is full.......waiting......')
                condition.wait()
            queue.append(i)
            print(f'Producer: Added item {i}. Queue size: {len(queue)}')
            condition.notify()



def consumer():
    """Removes and processes items from the queue."""
    while True:
        with condition:
            # Wait if the queue is empty
            if not queue:
                print("Consumer: Queue is empty. Waiting...")
                condition.wait()
            
            # Process an item
            item = queue.popleft()
            print(f"Consumer: Processed item {item}. Queue size: {len(queue)}")
            
            # Notify the producer that space is now available
            condition.notify()
            
            # Exit loop after processing enough items
            if item == 19:
                break


producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()

print("\nAll tasks completed.")
