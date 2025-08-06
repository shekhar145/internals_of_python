# Multiprocessing Supports two types of communication channel between processes:-
# 1. Queue      2. Pipes

## Queue:-

# Queues are thread and process safe. Any object put into a multiprocessing queue will be serialized.


# Use cases:

# Task distribution: A main process can fill a queue with tasks, and multiple worker processes can pull and process them.

# Collecting results: Worker processes can put their results into a queue, and a main process can collect and aggregate them.

# Inter-process communication: Processes can send messages, data, or even control signals to each other.

## Example:- let simulate a web crowler where producer will put urls in queue and consumers will process them and put result back in output queue

import time
import requests
import os
from multiprocessing import Process, Queue

def help_process_url(url: str) -> dict[str, str]:
    print(f"[{os.getpid()}] Processing: {url}")
    try:
        response = requests.get(url, timeout=5)
        time.sleep(1)
        return {
                "url": url,
                "status_code": response.status_code,
                "content_length": len(response.text)
            }
    except requests.exceptions.RequestException as e:
        print(f"[{os.getpid()}] Failed to process {url}: {e}")
        return {
                "url": url,
                "error": str(e)
            }
    
def producer(task_queue: Queue, urls: list[str], total_consumers: int):
    for url in urls:
        task_queue.put(url)

    # for gracefully shutdown it's a common pattern to put None in Queue for all consumers ad handle this condition in consumer code
    for _ in range(total_consumers):
        task_queue.put(None)

    print(f"[{os.getpid()}] Producer finished adding all tasks.")

def consumer(task_queue: Queue, result_queue: Queue):
    print(f"[{os.getpid()}] Consumer started...")
    while True:
        curr_task = task_queue.get()

        # handling None condition here
        if curr_task is None:
            break

        result = help_process_url(curr_task)
        result_queue.put(result)
    print(f"[{os.getpid()}] Consumer finished.")


if __name__ == '__main__':
    urls_to_crawl = [
        "https://www.google.com",
        "https://www.github.com",
        "https://www.python.org",
        "https://www.wikipedia.org",
        "https://www.linkedin.com",
        "https://www.bing.com",
        "https://www.stackoverflow.com",
        "https://www.nytimes.com",
        "https://www.openai.com",
        "https://www.apple.com"
    ]

    task_queue = Queue()
    result_queue = Queue()
    
    num_consumers = 4

    # A process for producer and start appending data to task queue
    producer_p = Process(target=producer, args=(task_queue, urls_to_crawl, num_consumers))
    producer_p.start()

    
    consumer_processes = []
    # starting new consumer processes

    for _ in range(num_consumers):
        p = Process(target=consumer, args=(task_queue, result_queue))
        p.start()
        consumer_processes.append(p)

    # Wait for the producer to finish
    producer_p.join()
    print("Producer process has finished.")


    for p in consumer_processes:
        p.join()

    final_result = []
    while not result_queue.empty():
        final_result.append(result_queue.get())

    print(final_result)

