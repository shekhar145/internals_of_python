import threading
import time

def crawl(link, delay=3):
    print(f"Starting to crawl {link}")
    time.sleep(delay)  # Simulate network delay
    print(f"Finished crawling {link}")

links = [
    "https://python.org",
    "https://github.com",
    "https://stackoverflow.com"
]

threads = []

for link in links:
    t = threading.Thread(target=crawl, args=(link,), kwargs={'delay': 2})
    threads.append(t)

# start each thread
for thread in threads:
    thread.start()

print('Total running thread',threading.active_count())
# above line output is 4 -> 3 + 1(main thread)



# wait for all threads to complete
for t in threads:
    t.join()

# Only 1 thread can execute python code at once, however threading is still an appropriate model if you want to run multiple I/O bound tasks simultaneously
