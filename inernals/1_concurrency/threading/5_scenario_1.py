"""

I will give you a scenario-based question and explain how to apply a `Condition` object to solve it, which is the kind of problem you might face in an SDE-3 interview.

***

### The Scenario: A Distributed Task Queue with Backpressure

Imagine you're designing a critical part of a large-scale data processing pipeline. You have multiple worker services that are processing data, but they can get overwhelmed. To manage this, you've decided to use a local, in-memory queue that acts as a buffer.

**The Setup:**
* A single **producer thread** ingests data from a network stream at a high, variable rate.
* Multiple **consumer threads** (a thread pool) process the data and send it to a backend service.
* The **in-memory queue** has a fixed, maximum capacity.

**The Challenge:**
How do you implement this system so that it handles the following conditions efficiently and correctly without losing data or wasting CPU resources?

1.  **Queue is Full (Backpressure):** If the producer is faster than the consumers, the queue will fill up. The producer **must block** and wait for space to become available. It should not drop data.
2.  **Queue is Empty:** If the consumers are faster than the producer, they will empty the queue. The consumers **must block** and wait for new data to arrive. They should not repeatedly check the queue in a tight loop (busy-waiting).
3.  **Dynamic Workload:** The processing time for each item can vary greatly, and the network stream can be inconsistent. The solution must be robust to these fluctuations.

**Interview Question:** "Design and implement this buffered queue system using Python's `threading` library. Your solution must be thread-safe, prevent busy-waiting, and handle backpressure gracefully. Explain your choice of synchronization primitives."

### Solution and `Condition` Object Application

This problem is a classic application of the producer-consumer pattern, and the `Condition` object is the most appropriate tool.

Here's a breakdown of how to structure your answer for an SDE-3 interview:

1.  **Initial Design & Data Structures:**
    * State that you'll use a `collections.deque` for the queue because it's a thread-safe, efficient, double-ended queue.
    * Explain the need for a synchronization primitive to manage the state of the queue.

2.  **Choice of Synchronization Primitive:**
    * Rule out simple `Lock`s: A `Lock` only provides mutual exclusion. It can't make a thread wait for a specific condition (e.g., "queue is not empty" or "queue is not full"). You would have to use `while True` loops with `time.sleep()`, which is inefficient busy-waiting.
    * Explain why `Condition` is the best choice:
        * It combines a `Lock` with a `wait()`/`notify()` mechanism.
        * It allows threads to go to sleep efficiently and only be woken up when a specific condition is met.

3.  **Implementation Details (The Code):**

    * **The Shared `Condition`:** A single `threading.Condition` object will be shared between all producer and consumer threads. 
    * **Producer Logic:**
        * The producer must first **acquire the condition's lock** using a `with condition:` block.
        * Inside the block, it will use a **`while` loop** with the condition `len(queue) == MAX_CAPACITY`.
        * If the condition is `True`, it calls `condition.wait()` to block. The `wait()` method atomically releases the lock and puts the thread to sleep.
        * Once an item is successfully added, it calls `condition.notify()` to signal to a waiting consumer that an item is available.
    * **Consumer Logic:**
        * Each consumer thread must also **acquire the same lock**.
        * It will use a **`while` loop** with the condition `not queue`.
        * If the queue is empty, it calls `condition.wait()` to block and sleep.
        * Once an item is successfully removed, it calls `condition.notify()` to signal to the producer that space is now available.

4.  **Handling Spurious Wakeups (Advanced Detail):**
    * Mention that `wait()` can sometimes return even if `notify()` or `notify_all()` was not called (a "spurious wakeup").
    * Explain that the `while` loops are the correct way to handle this, as the thread will re-check the condition immediately upon waking up and re-enter the `wait()` state if the condition is still not met. This demonstrates a deep understanding of thread synchronization subtleties.

5.  **Conclusion:**
    * Summarize the solution's benefits: The `Condition` object provides a clean, robust, and efficient way to coordinate threads based on the state of the shared queue. It avoids busy-waiting, handles variable loads, and prevents the buffer from overflowing, meeting all the requirements of the problem. This shows the interviewer you can not only code but also design a scalable, reliable system.

"""