Difference between Thread and Process

Feature	Processes	Threads
Isolation	High (isolated memory space)	Low (shared memory space)
Resources	Own resources (memory, file handles, etc.)	Shared resources of the parent process
Creation	Slow, high overhead	Fast, low overhead
Communication	Complex (IPC required)	Simple (direct memory access)
Context Switching	Slow, high overhead	Fast, low overhead
Use Case	Running separate, independent applications	Running multiple tasks within a single application (e.g., UI responsiveness, background tasks)


GIL:- 
Gloabal Interpreter Lock, is a mutex lock that protect access to Python objects, preventing mutliple native threads from executing python bytecode at the same time.
This means that even on a machine with multiple CPU cores, only 1 thread can be actively running Python code at any given moment.

The GIL was created to simplify Python's memory management and garbage collection. By ensuring only one thread can modify objects at a time, it avoids the need for complex and potentially slow fine-grained locking on every object.

The GIL has a significant impact on how you use multithreading in Python:

For I/O-bound tasks (e.g., network requests, reading from a disk): Multithreading is very effective. When a thread performs an I/O operation, it releases the GIL, allowing another thread to run. This means that while one thread is waiting for data, others can make progress.

For CPU-bound tasks (e.g., mathematical calculations, heavy data processing): Multithreading provides little to no performance benefit. Because the GIL ensures only one thread can execute bytecode at a time, a program running on a multi-core machine will still be limited to a single core for its Python computation. For these tasks, you should use the multiprocessing module, which bypasses the GIL by using separate processes.

multithreading does not completely bypass the GIL. In fact, the GIL is a fundamental part of Python's multithreading implementation.


The GIL is a mutex (a type of lock) that ensures only one thread can execute Python bytecode at a time, even on a multi-core processor. This means that Python threads cannot run in true parallel.


How Threads Interact with the GIL
GIL Acquisition: To execute Python code, a thread must first acquire the GIL.

GIL Release: A thread will release the GIL in a few key scenarios:

I/O Operations: When a thread is waiting for an external resource (like a network response or a file read), it releases the GIL. This is the main reason why multithreading is effective for I/O-bound tasks. While one thread is waiting, another can acquire the GIL and run.

Timed Slices: Python's interpreter has a mechanism to force a thread to release the GIL after a certain number of bytecode instructions have been executed. This prevents a single, long-running thread from monopolizing the CPU and starving other threads

Threading:-
1. Multiple thread of conyrol sharing their global data space.
2, For synchronization, we use locks, semaphores, and condition variables.
3. Threading module provides a way to run multiple threads (lightweight processes) in a single process. It allows   for the creation and management of threads, making it possible to execute tasks in parallel, sharing memory space.
4. Threads are particular useful when tasks are I/O bound, such as file operations for making network requests, where much of the time is spent waiting for external resources.

When to Use RLock vs. Lock
Use RLock when you need to acquire a lock from within a function that might already be holding that same lock. This is common in complex object models or recursive algorithms.

Use Lock for most other synchronization needs. A standard Lock is slightly more efficient and should be preferred unless re-entrancy is explicitly required. Using a standard lock can also help you identify potential design issues where a function might be trying to acquire a lock it already holds, which could be a sign of a logic error.