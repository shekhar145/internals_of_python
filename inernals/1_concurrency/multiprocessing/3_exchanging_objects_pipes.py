# A Pipe creates a two-way communication channel between two processes. It returns a pair of connection objects, each representing one end of the pipe. Data written on one end is available to be read on the other.

# How it works: One process uses conn.send(obj) to send an object and the other uses conn.recv() to receive it. It's a point-to-point connection, meaning it's designed for communication between exactly two processes.

# Use cases:

# Direct communication: When you need a dedicated, bidirectional channel between a parent and a child process, or two specific processes.

# Request-response patterns: A child process can wait for a request from the parent, perform an action, and send a response back.sourcve


# Create a 2-way pipeline for image processing service, where parent process will send the commands to it and consumer will act and send back the response

import os
import time
from multiprocessing import Process, Pipe

def consumer_image_processor(conn):
    image = b'R0lGODlhAQABAIABAP///wAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
    try:
        while True:
            command: str = conn.recv()

            if command == 'exit':
                print(f"[{os.getpid()}] Exit command received. Shutting down.")
                break

            elif command.startswith('resize'):
                conn.send({'success':{
                    'status': 'success',
                    'size': 'new size',
                    'message': 'image resized successfully'
                }})
            
            elif command.startswith('greyscale'):
                conn.send({'success': {
                    'status': 'success',
                    'message': 'image greyscaled successfully'
                }})
            else:
                conn.send({'success':{
                        "success": False,
                        "error": f"Unknown command: {command}"
                    }})
    except EOFError:
        # Parent closed the connection
        print(f"[{os.getpid()}] Parent connection closed. Exiting.")
    except Exception as e:
        print(f"[{os.getpid()}] An error occurred: {e}")
    finally:
        conn.close()
            
if __name__ == '__main__':
    print(f"[{os.getpid()}] Main process started.")

    parent_conn, child_conn = Pipe()

    child_p = Process(target=consumer_image_processor, args=(child_conn,))
    child_p.start()


    # Communication:
    try:
        parent_conn.send('resize')

        # recieve response
        response = parent_conn.recv()
        if response.get("success"):
            print(f"[{os.getpid()}] Received resized image (size: {response['success']})")
            # You can save the image if you want:
            # with open("resized_image.png", "wb") as f:
            #     f.write(response['data'])
        else:
            print(f"[{os.getpid()}] Error: {response}")
        time.sleep(1) # Simulate some other work

        parent_conn.send('greyscale')
        response = parent_conn.recv()
        if response.get("success"):
            print(f"[{os.getpid()}] Received resized image (size: {response['success']})")
            # You can save the image if you want:
            # with open("resized_image.png", "wb") as f:
            #     f.write(response['data'])
        else:
            print(f"[{os.getpid()}] Error: {response}")
        time.sleep(1) # Simulate some other work
    finally:
        # 4. Send the "exit" command to shut down the worker gracefully
        print(f"\n[{os.getpid()}] Sending 'exit' command to worker...")
        parent_conn.send("exit")
        
        # Close the parent's end of the pipe
        parent_conn.close()
        
        # Wait for the worker process to terminate
        child_p.join()


        