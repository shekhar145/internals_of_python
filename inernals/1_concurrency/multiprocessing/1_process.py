# how to create and start a process
from multiprocessing import Process
import os

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)

if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()

# Why this program will not work without __name__ == 'main'


"""
Python's multiprocessing module creates new processes in one of three main ways

1. fork (on Unix-like systems like Linux): A new child process is created as a copy of the parent process. 
It inherits the entire memory space, open file descriptors, and state. 
The child process then continues from where the parent process left off (specifically, it starts executing the code immediately after the fork call).
Note that safely forking a multithreaded process is problematic
Changed in version 3.12: If Python is able to detect that your process has multiple threads, the os.fork() function that this start method calls internally will raise a DeprecationWarning

2. spawn (the default on Windows and macOS, and an option on Linux): A brand new Python interpreter process is started. 
The parent process's code is effectively re-imported and re-executed from the beginning in this new child process.
 Starting a process using this method is rather slow compared to using fork or forkserver.


 3. Forkserver:- In starting a server process is spawned. 
 From then on, whenever a new process is needed, the parent process connects to the server and requests that it fork a new process. 
 The fork server process is single threaded unless system libraries or preloaded imports spawn threads as a side-effect so it is generally safe for it to use os.fork(). 
 No unnecessary resources are inherited.


The Problem with spawn:-
Without __name=='main' block, child process reexecute the entire script from the top. and when it encounter p = Process(target=f, args=('bob',)),
it would create another child process. This child process then reexecute the entire script and then create another child process and so on.
This would lead to infinite loop of process creation, quickly consuming all system resource and crashing your program.


How __name='main' will is helpful:
When first time script run your module name is process, so code inside if block will execute and it create a new child process
this time child process when child process run the cript from start it can't execute if block because it's not the default main process so no inifinite loop.


Even on Linux, where fork is the default, it's considered a best practice to include this check for portability and to avoid potential issues in more complex scenarios.


"""


# Leaked Resources and Resource Trancker
"""

### The Core Problem: "Leaked" Resources

Imagine you have a program that creates temporary, named resources that are shared between different parts of the program. Think of these as special "files" that exist in the computer's memory or file system, like:

* **Named semaphores:** A kind of lock used to coordinate access to a shared resource.
* **`SharedMemory` objects:** A block of memory that multiple processes can read from and write to.

Normally, when your program finishes, it should "clean up" and delete these temporary resources. However, what if one of your processes crashes or is killed unexpectedly (e.g., by a `kill` command or a system error)? This process might not have a chance to clean up its resources, leaving them behind. This is what the text calls a **"leaked" resource**.

### Why Leaked Resources are a Problem

Leaked resources are a bad thing for two main reasons:

1.  **Limited System Resources:** Your operating system (OS) has a finite limit on how many of these named semaphores and shared memory segments can exist at one time. If you keep leaking them, you could eventually hit this limit, and new programs won't be able to create these resources, causing them to fail.
2.  **Wasted Memory:** Leaked `SharedMemory` segments continue to occupy space in your computer's main memory, even if no program is using them. This is wasted memory that can't be used for other tasks.

These leaks are especially problematic because the OS won't automatically clean them up until the next time you restart the computer.

### The Solution: The "Resource Tracker"

This is where the `multiprocessing` module's **resource tracker process** comes in.

* **What it is:** A special, separate process that the `multiprocessing` module automatically starts for you when you use the `spawn` or `forkserver` start methods on a POSIX system (like Linux or macOS).
* **What it does:** Its sole job is to **keep a list of all the named resources** (like semaphores and shared memory) that have been created by your program's various processes. It "tracks" them.
* **How it helps:** When your entire program finishes (meaning all the processes you created have exited), the resource tracker process wakes up and checks its list. It then **cleans up any resources that are still on its list**.

### The "Killed by a Signal" Scenario

The text specifically mentions this because it's the most common cause of leaks. If a process is killed by a signal (e.g., a `SIGKILL`), it's immediately terminated without being given a chance to run its cleanup code. The resource tracker is the safety net for this exact situation. It will see that the parent process has finished but some resources are still on its list, and it will unlink them, preventing them from becoming a permanent leak.

### Summary

The **resource tracker** is a dedicated cleanup crew. It watches over all the shared resources created by your program. If one of your processes crashes and leaves a mess behind (a "leaked" resource), the resource tracker will automatically clean it up for you once your main program is done, preventing your system from being cluttered with permanent, wasted memory and hitting resource limits. It's a crucial part of the `multiprocessing` module's design to ensure stability and good resource management.

"""