"""
 let's consider a scenario where multiple threads process data, and each thread needs its own unique identifier and a counter that is not shared with other threads.

In this example, we'll simulate a worker pool that processes tasks. Each worker thread will have a thread-local ID and a counter to track how many tasks it has processed.



Imagine a system that handles incoming requests. We want to:

1. Assign a unique ID to each worker thread.

2. Count the number of requests processed by each individual thread, not the total number across all threads.

3. Store this data in a way that's thread-safe and isolated, so one thread's count doesn't affect another's.

Using threading.local is the ideal solution because it gives each thread its own private storage space for the ID and counter.
"""

import threading
import time
import random

thread_data = threading.local()

wordker_id_counter = 0
wordker_id_lock = threading.Lock()

def get_next_worker_id():
    global wordker_id_counter
    with wordker_id_lock:
        wordker_id_counter += 1
        return wordker_id_counter
    
def process_task():
    print(f"Worker {thread_data.worker_id}")
    time.sleep(random.uniform(0.1, 0.5))
    thread_data.tasks_processed += 1

def worker_thread(num_tasks: int):
    thread_data.worker_id = get_next_worker_id()
    thread_data.tasks_processed = 0

    print(f"Worker {thread_data.worker_id} has started.")
    for _ in range(num_tasks):
        process_task()

    print(f"Worker {thread_data.worker_id} finished. Total tasks processed: {thread_data.tasks_processed}")

if __name__== "__main__":
    num_of_tasks = 5
    threads = []

    for i in range(3):
        thread = threading.Thread(target=worker_thread, args=(num_of_tasks+i,))
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()