"""

The multiprocessing.Manager is a powerful tool for sharing complex Python objects between processes. While multiprocessing.Queue and Pipe are great for passing messages or simple data, they aren't suitable for managing a single, shared object like a list, dictionary, or a lock that needs to be updated by multiple workers. The Manager provides a way to create and manage these "shared" objects.

The core idea is that a Manager object starts a dedicated server process that holds the actual shared objects in its memory. Other processes in your program then communicate with this server process through proxies. When you access or modify an attribute of a managed object, the proxy object sends a message to the server process, which performs the operation on the real object and sends back the result. This client-server architecture ensures that all access is synchronized and thread/process-safe.

Key Characteristics
Shared Objects: It enables processes to share complex data structures like list, dict, Lock, Event, Semaphore, and even custom classes, as long as they are "pickleable."

Proxy Objects: The Manager doesn't give you the real object. Instead, it gives you a proxy object that looks and acts just like the original, but all its method calls are forwarded to the manager's server process.

Synchronization: The server process handles all the necessary locking and synchronization, preventing race conditions when multiple processes try to modify the same object simultaneously.

Automatic Cleanup: It is best used with a with statement, which guarantees that the manager's server process is properly shut down when it's no longer needed, preventing resource leaks.

Internal Handling of multiprocessing.Manager
The Manager's internal handling is a classic example of a client-server model for distributed objects.

Server Process Creation: When you instantiate a Manager (e.g., multiprocessing.Manager()), it starts a background process. This is the manager server process. This process's sole purpose is to create and manage the shared objects requested by other processes. It runs a loop, listening for incoming requests from other processes.

Object Creation: When a process calls a method on the manager, such as manager.dict() or manager.list(), it sends a request to the server process. The server process then creates the actual dictionary or list in its own memory space.

Proxy Generation: The server process then sends a special proxy object back to the requesting process. This proxy object holds a reference to the actual object on the server.

Method Invocation: When a worker process calls a method on the proxy object (e.g., shared_dict['key'] = 'value'), the proxy object pickles the method call and its arguments and sends this message to the server process.

Execution and Response: The server process receives the message, un-pickles it, and executes the actual method on the real object in its memory. If the method returns a value (e.g., a dictionary value), the server pickles that value and sends it back to the client process. The client's proxy then un-pickles the result and returns it.

This complex but robust system allows for seamless, synchronized access to shared data without the pitfalls of shared memory or race conditions.

"""

# Example

# Multiple worker processes need to update a shared ststus or result dictionary
import multiprocessing
import time
import random

def worker(worker_id: int, shared_dict_results: dict[str, str]):
    task_duration = random.uniform(1,3)
    time.sleep(task_duration)

    shared_dict_results[f"worker_{worker_id}"] = f"Completed task after {task_duration:.2f}s"
    print(f"Process {worker_id} has processed the result")

if __name__ == '__main__':
    with multiprocessing.Manager() as manager:
        shared_results = manager.dict()

        num_workers = 5
        processes = []

        for i in range(num_workers):
            p = multiprocessing.Process(target=worker, args=(i, shared_results))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        for worker_key, result in shared_results.items():
            print(f"{worker_key}  - {result}")

            
