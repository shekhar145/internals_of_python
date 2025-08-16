"""
A thread pool is a design pattern used in software development to manage a set of worker threads. Instead of creating a new thread for every incoming task, a thread pool maintains a fixed number of pre-existing threads. When a new task arrives, it's placed in a queue, and one of the available threads from the pool picks it up and executes it. 🧵

This approach is highly effective for improving application performance and resource management, especially in applications that handle many short-lived tasks, such as web servers or concurrent data processing pipelines.

Key Components of a Thread Pool
Worker Threads: A fixed number of threads that are created at the start of the program and are ready to execute tasks. These threads are the "workers" of the pool.

Task Queue: A thread-safe queue (like Python's queue.Queue) where incoming tasks are placed. The queue acts as a buffer between the main application and the worker threads.

Manager: The component that orchestrates everything. It's responsible for creating the worker threads, assigning tasks from the queue to available workers, and managing the lifecycle of the pool.

Advantages of Using a Thread Pool
Reduced Overhead: Creating a new thread is a computationally expensive operation. A thread pool avoids this overhead by reusing existing threads, which significantly improves performance, especially for a high volume of short tasks.

Resource Management: It prevents the system from being overwhelmed by a flood of threads. By setting a fixed pool size, you can control the maximum number of concurrent operations, which helps manage system resources like CPU and memory.

Improved Responsiveness: The main application thread can submit tasks to the queue and continue its work immediately without waiting for the task to be completed.

Concurrency Control: It allows you to control the level of concurrency in your application. For example, you can limit the number of database connections to prevent overwhelming the database server.
"""

import concurrent.futures
import threading
import time

def worker_function(task_id):
    print(f"Worker {threading.get_ident()}: Starting task {task_id}")
    time.sleep(1) # Simulate some work
    print(f"Worker {threading.get_ident()}: Finishing task {task_id}")
    return f"Task {task_id} completed"

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    tasks = [f"Task-{i}" for i in range(10)]
    results = executor.map(worker_function, tasks)

    for result in results:
        print("main thread", result)

print("All tasks have been processed.")