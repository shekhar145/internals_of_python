"""
apply_async() is a non-blocking version of apply(). It's useful when you want to submit tasks and get the results later, without waiting for each one to finish. This is good for "fire-and-forget" style tasks or when you have other work to do while the workers are busy.

"""


import multiprocessing
import time
import random

def worker_task(task_id):
    """A worker function that simulates a variable amount of work."""
    duration = random.uniform(0.5, 2.0)
    print(f"Task {task_id} started, sleeping for {duration:.2f}s...")
    time.sleep(duration)
    result = f"Task {task_id} finished after {duration:.2f}s."
    print(result)
    return result

if __name__ == '__main__':
    num_tasks = 5
    results_list = []
    
    with multiprocessing.Pool(processes=4) as pool:
        print("Main process submitting tasks...")
        
        # Submit tasks using apply_async, which returns an AsyncResult object immediately
        async_results = [pool.apply_async(worker_task, args=(i,)) for i in range(num_tasks)]
        
        print("Main process is now free to do other work while tasks run...")
        # Simulate some other work
        time.sleep(1)
        
        print("\nMain process is now collecting results...")
        # Get the results from the AsyncResult objects.
        # .get() will block until the result is available.
        for async_res in async_results:
            results_list.append(async_res.get())
            
    print("\nAll tasks are completed.")
    print("Final results list:")
    for res in results_list:
        print(res)


"""
What this example shows:

apply_async() is used to submit tasks without waiting for a result.

The main process can continue its execution (time.sleep(1)) while the workers are running in the background.

The async_results list holds AsyncResult objects, which are promises to get a result later.

The result.get() method is used to block and retrieve the result for each task when it's needed. This is a powerful pattern for more complex workflows where tasks don't all need to be completed at once.


"""