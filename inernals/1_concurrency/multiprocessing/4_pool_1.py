"""
The multiprocessing.Pool in Detail
The multiprocessing.Pool is a higher-level, more convenient way to parallelize a task that can be broken down into many independent sub-tasks. It manages a fixed number of worker processes, providing a "pool" of ready-to-go workers that can be assigned tasks as they become available. This is particularly useful for what are known as "embarrassingly parallel" problems—problems where the sub-tasks don't depend on each other and can be run simultaneously without needing to communicate.

Key Characteristics
Worker Management: You don't create or manage individual Process objects. The Pool handles creating, starting, and shutting down the worker processes automatically.

Load Balancing: The Pool automatically distributes tasks to available workers. If a worker finishes a task, it's immediately given the next one from the queue. This is a very efficient form of load balancing.

Synchronization: The Pool handles the necessary synchronization and communication mechanisms (like queues) internally, so you don't have to manage them yourself.

Task-Oriented Methods: It provides a set of powerful methods for distributing tasks, such as map(), starmap(), apply(), and apply_async().

The multiprocessing.Pool in Detail
The multiprocessing.Pool is a higher-level, more convenient way to parallelize a task that can be broken down into many independent sub-tasks. It manages a fixed number of worker processes, providing a "pool" of ready-to-go workers that can be assigned tasks as they become available. This is particularly useful for what are known as "embarrassingly parallel" problems—problems where the sub-tasks don't depend on each other and can be run simultaneously without needing to communicate.

Key Characteristics
Worker Management: You don't create or manage individual Process objects. The Pool handles creating, starting, and shutting down the worker processes automatically.

Load Balancing: The Pool automatically distributes tasks to available workers. If a worker finishes a task, it's immediately given the next one from the queue. This is a very efficient form of load balancing.

Synchronization: The Pool handles the necessary synchronization and communication mechanisms (like queues) internally, so you don't have to manage them yourself.

Task-Oriented Methods: It provides a set of powerful methods for distributing tasks, such as map(), starmap(), apply(), and apply_async().

Internal Handling of multiprocessing.Pool
The Pool is not a magic black box; it's a clever wrapper around the same core multiprocessing concepts we've already discussed. Here's a simplified look at its internal workings:

Creation: When you create a Pool object (e.g., multiprocessing.Pool(processes=4)), the Pool immediately creates and starts a specified number of worker processes. It also creates a task queue and a results queue internally. Each worker is given access to these two queues.

The map() Method: The map() method is the workhorse of the Pool.

Task Producer: The map() call in the main process takes an iterable (e.g., a list of numbers) and your target function. It then puts each item from the iterable, along with the target function's name and arguments, into the internal task queue.

Worker Consumer: Each worker process sits in a loop, continuously trying to get() a task from the task queue.

Task Execution: When a worker gets a task (e.g., (calculate_square, 5)), it executes the function with the given arguments.

Result Producer: After the worker completes the task, it takes the return value and puts it into the internal results queue.

Main Process Consumer: The map() method in the main process then blocks and waits. It continuously get()s results from the results queue.

Result Ordering: The Pool's internal mechanism ensures that the results are returned to the main process in the correct order, matching the order of the input iterable. This is a key feature of map().

Shutdown: When the Pool is closed (e.g., via the with statement or explicitly calling pool.close()), a special "sentinel" value is put into the task queue for each worker. The workers, upon receiving this sentinel, gracefully shut down. pool.join() then blocks until all workers have finished and exited.

In essence, a Pool is a pre-built producer-consumer framework. The main process is the producer of tasks, the worker processes are the consumers of tasks, and the Pool handles the queues and synchronization for you, making your code much cleaner.

Good Examples of multiprocessing.Pool
Here are two practical examples demonstrating different use cases of the Pool.

Example 1: Simple map() for CPU-Bound Tasks
This is the most common use case. We'll use the prime number checking problem to show how Pool simplifies it.





"""





import multiprocessing
import time
import math

def is_prime(number):
    """
    A function to check if a number is prime using trial division.
    This is a CPU-bound task.
    """
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
        
    for i in range(3, int(math.sqrt(number)) + 1, 2):
        if number % i == 0:
            return False
            
    return True

if __name__ == '__main__':
    # Define a large range of numbers to test
    start_num = 2
    end_num = 1_000_000
    numbers_to_check = range(start_num, end_num + 1)
    
    # Get the number of available CPU cores
    num_cores = multiprocessing.cpu_count()
    print(f"Using a pool of {num_cores} worker processes.")
    
    start_time = time.time()
    
    # Create a Pool of worker processes. The 'with' statement
    # ensures the pool is properly managed and closed.
    with multiprocessing.Pool(processes=num_cores) as pool:
        # pool.map() distributes the 'is_prime' function to each
        # number in 'numbers_to_check'.
        # It's a blocking call that returns all results in order.
        is_prime_results = pool.map(is_prime, numbers_to_check)
        
    end_time = time.time()
    
    # The results are booleans, so we can count the primes
    prime_numbers = [num for num, is_p in zip(numbers_to_check, is_prime_results) if is_p]
    
    print(f"\nFound {len(prime_numbers)} primes between {start_num} and {end_num}.")
    print(f"Total time taken: {end_time - start_time:.4f} seconds.")
    print("First 10 primes:", prime_numbers[:10])