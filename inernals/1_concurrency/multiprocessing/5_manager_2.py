# Example 2:- sharing a lock to protect a Non-Managed Resource

# Sometimes we need to provide a user-provided lock to protect a resource that isn't itself managed
# Normal threading.Lock will not work here, because threads shared menory so it will be stored in a single process's memory
# Manager provide a safe lock for process


import multiprocessing
import time

def write_to_file(lock, filename, process_id):
    with lock:
        with open(filename, 'a') as f:
            for i in range(5):
                f.write(f'Process {process_id} is writing')
                time.sleep(0.1)
            f.write(f'Process {process_id} finished writing')

if __name__ == '__main__':
    filename = 'shared_log.txt'
    with open(filename, 'w') as f:
        f.write('--- Shared Log Start ----')

    with multiprocessing.Manager() as manager:
        lock = manager.Lock()

        num_of_process = 5
        processes = []

        for i in range(num_of_process):
            p = multiprocessing.Process(target=write_to_file, args=(lock, filename, i))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()
        print("All workers finished. Check 'shared_log.txt' for the output.")

        
