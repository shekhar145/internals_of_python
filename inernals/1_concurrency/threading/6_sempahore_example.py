# log rotation

import threading
import time
import os
import queue
from datetime import datetime
import logging

# --- Configuration ---
LOG_FILE = "app.log"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB for this example
ROTATION_INTERVAL = 60  # seconds
INGESTION_QUEUE = queue.Queue()

# --- Shared resources ---
_log_lock = threading.Lock() # Protects log file writes

# --- Mock Ingestion Service ---
# In a real system, this would be a separate microservice
# with its own threads, network calls, and retries.
def mock_ingest_service():
    while True:
        try:
            rotated_file = INGESTION_QUEUE.get(timeout=5)
            print(f"Ingestion Service: Received file '{rotated_file}'. Ingesting...")
            
            # Simulate network call and ingestion
            time.sleep(1) 
            
            print(f"Ingestion Service: Successfully ingested and deleting '{rotated_file}'.")
            os.remove(rotated_file)
            INGESTION_QUEUE.task_done()
        except queue.Empty:
            pass
        except Exception as e:
            print(f"Ingestion Service: Failed to ingest file. Retrying later. Error: {e}")
            # In a real system, you would push the file back to the queue or a dead-letter queue
            INGESTION_QUEUE.put(rotated_file)

# --- The Client-Side Agent ---
class LogAgent:
    def __init__(self):
        self.writer_thread = threading.Thread(target=self._log_writer, daemon=True)
        self.rotator_thread = threading.Thread(target=self._file_rotator, daemon=True)
        self.writer_thread.start()
        self.rotator_thread.start()

    def log(self, message):
        """Public method for the application to log messages."""
        with _log_lock:
            with open(LOG_FILE, "a") as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"[{timestamp}] {message}\n")

    def _log_writer(self):
        """Worker thread that continuously writes logs from an internal buffer."""
        # For simplicity, we directly write to file here.
        # In a real system, this would read from an in-memory queue.
        while True:
            time.sleep(0.1)

    def _file_rotator(self):
        """Worker thread that handles log rotation based on size or time."""
        while True:
            time.sleep(1) # Check frequently
            try:
                # Atomicity check: use a lock to ensure no writes happen during rotation
                with _log_lock:
                    if os.path.getsize(LOG_FILE) >= MAX_FILE_SIZE:
                        self._perform_rotation()
            except FileNotFoundError:
                # Handle the case where the file is rotated or not yet created
                pass
            except Exception as e:
                print(f"File Rotator: Error during rotation: {e}")

    def _perform_rotation(self):
        """Performs the atomic file rotation."""
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        new_filename = f"{LOG_FILE}.{timestamp}"
        
        # Atomic rename on Linux: os.rename() is atomic
        # On Windows, you might need a different approach for true atomicity
        try:
            os.rename(LOG_FILE, new_filename)
            print(f"Rotated '{LOG_FILE}' to '{new_filename}'.")
            # Push the rotated file path to the ingestion queue
            INGESTION_QUEUE.put(new_filename)
        except FileNotFoundError:
            print(f"Error: Log file '{LOG_FILE}' not found during rotation.")
            return

        # Create a new, empty log file for continued logging
        with open(LOG_FILE, "w") as f:
            pass

# --- Main Application Logic (Simulating a service) ---
if __name__ == "__main__":
    # Start the log agent
    log_agent = LogAgent()
    
    # Start the mock ingestion service thread
    ingestor = threading.Thread(target=mock_ingest_service, daemon=True)
    ingestor.start()

    print("Log Agent started. Generating log messages...")
    try:
        # Simulate the application generating logs
        for i in range(1000):
            message = f"This is log message number {i}. This message is long enough to fill the file quickly."
            log_agent.log(message)
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Application shutting down.")
    finally:
        # Wait for any pending ingestion to complete
        INGESTION_QUEUE.join()
        print("All pending files have been ingested.")