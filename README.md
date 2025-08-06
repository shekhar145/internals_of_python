# internals_of_python
Implementation of some core concepts of python

### Project Plan: Internals of Python

**Goal:** Implement a simplified version of Python's core libraries and concepts to demonstrate a deep understanding of the language's internals.

---

### **1. Concurrency (Multiprocessing & Threading)**

This is a great starting point as it's a critical and often misunderstood area of Python.

* **Sub-topics:**
    * **Multiprocessing:**
        * Implement a simple `Process` class with `start()`, `join()`, and `is_alive()` methods.
        * Create a simple `Queue` for inter-process communication.
        * Implement `Pool` and `map` for parallel task execution.
    * **Threading:**
        * Implement a simplified `Thread` class with `start()`, `join()`, and `is_alive()`.
        * Implement `Lock` and `RLock` for thread synchronization.
        * Implement a simple `Event` class for signaling between threads.
        * Demonstrate the Global Interpreter Lock (GIL) and explain its implications with a simple example.

---

### **2. Asynchronous Programming**

This topic directly builds on concurrency and is a cornerstone of modern, high-performance Python applications.

* **Sub-topics:**
    * **Event Loop:**
        * Implement a basic event loop from scratch.
        * Use a select-based or poll-based approach to monitor file descriptors (sockets).
        * Implement `async` and `await` with a generator-based approach.
    * **Coroutines:**
        * Implement a simple `Future` object to represent the result of an async operation.
        * Demonstrate how coroutines are scheduled on the event loop.
        * Implement a basic version of `asyncio.sleep()` and `asyncio.gather()`.

---

### **3. Data Structures**

Demonstrating how Python's fundamental data structures are built shows an understanding of memory management and performance trade-offs.

* **Sub-topics:**
    * **Lists:**
        * Implement a dynamic array from scratch.
        * Show how `append()` and `pop()` work, including resizing and memory allocation.
    * **Dictionaries:**
        * Implement a simple hash map.
        * Explain the hash function and collision resolution strategies (e.g., open addressing or chaining).
        * Demonstrate how a dictionary resizes when it becomes too full.
    * **Sets:**
        * Implement a hash-based set.
        * Explain how membership checking (`in`) works in $O(1)$ average time.

---

### **4. Object Model**

This topic is crucial for a senior role. It shows you understand how Python objects are represented in memory.

* **Sub-topics:**
    * **`type` and `object`:**
        * Implement a simplified object model where every object has a type and a value.
        * Explain the relationship between `type`, `object`, and classes.
    * **`__new__` and `__init__`:**
        * Demonstrate the two-step object creation process.
        * Implement a simple metaclass.
    * **`__slots__`:**
        * Explain how `__slots__` works to save memory.
        * Implement a simplified version to show how the instance dictionary is bypassed.

---

### **5. Garbage Collection**

Memory management is a key aspect of any language, and this topic is a great way to showcase your knowledge.

* **Sub-topics:**
    * **Reference Counting:**
        * Implement a simple reference counting mechanism.
        * Show how `sys.getrefcount()` works.
        * Demonstrate the problem with circular references.
    * **Generational Garbage Collection:**
        * Explain the concept of generations.
        * Implement a simplified generational garbage collector to handle circular references.

---

### **6. Iterators & Generators**

This is a fundamental and widely used concept in Python.

* **Sub-topics:**
    * **Iterators:**
        * Implement a custom iterator class with `__iter__` and `__next__` methods.
        * Explain the `for` loop's underlying mechanism.
    * **Generators:**
        * Implement a simplified generator function using `yield`.
        * Explain the difference between a generator and a regular function.
        * Demonstrate generator expressions.

---

### **7. Context Managers (`with` statement)**

This is a great topic to show you understand resource management and clean code principles.

* **Sub-topics:**
    * **`__enter__` and `__exit__`:**
        * Implement a custom context manager class.
        * Explain how exceptions are handled within the `__exit__` method.
    * **`contextlib`:**
        * Implement a simplified version of `contextlib.contextmanager` using a generator and the `yield` statement.

---

### **8. Function Decorators**

A powerful feature of Python, decorators are a must-know for a senior role.

* **Sub-topics:**
    * **Simple Decorators:**
        * Implement a simple decorator to wrap a function and add functionality (e.g., logging).
    * **Decorators with Arguments:**
        * Show how to create a decorator that accepts arguments.
    * **Class-based Decorators:**
        * Implement a decorator using a class with `__call__` method.

---

### **9. Metaprogramming**

This topic is a great way to differentiate yourself and show a deep, advanced understanding of the language.

* **Sub-topics:**
    * **Metaclasses:**
        * Create a custom metaclass to automatically register classes or modify class attributes.
        * Explain how metaclasses control class creation.
    * **`__getattr__`, `__getattribute__`:**
        * Implement a proxy object using these magic methods.
        * Explain the difference between the two and when to use each.

---

### **10. Foreign Function Interface (FFI) & C Extensions (ctypes)**

While not strictly an "internal" of Python itself, this topic shows how Python integrates with other languages, which is common in high-performance or systems-level engineering.

* **Sub-topics:**
    * **`ctypes`:**
        * Write a simple C function (e.g., `add(int a, int b)`).
        * Use `ctypes` to load the shared library and call the C function from Python.
        * Explain data type mapping between Python and C.
    * **Extension Modules (Optional but highly impressive):**
        * Write a simple Python C extension module.
        * Demonstrate how to expose C functions to Python.

### How to use this for your project and interviews:

1.  **Structure your GitHub repository:**
    * Each main topic (e.g., `concurrency`, `asyncio`, `datastructures`) should be its own directory.
    * Inside each directory, create sub-directories for each sub-topic.
    * Use clear `README.md` files in each directory to explain the concept, your implementation, and any design decisions you made.
    * Include a main `README.md` for the project that outlines the overall goal and a high-level table of contents.

2.  **Write clear and concise code:**
    * Use type hints.
    * Include docstrings explaining the purpose of each class and method.
    * Add comments to highlight key logic, especially where your code deviates from the standard library's approach for simplicity.

3.  **Prepare for interviews:**
    * For each topic, be ready to explain the "why" behind your implementation. For example, "I chose a hash map for dictionaries because it provides $O(1)$ average-case lookup time, but this requires handling collisions, which I did with..."
    * Be ready to whiteboard a simplified version of your implementation.
    * Tie your project to a real-world problem. For example, "My simplified `asyncio` event loop is similar to how a web server handles multiple connections without blocking."

Good luck with your project! It's a challenging but highly rewarding endeavor.