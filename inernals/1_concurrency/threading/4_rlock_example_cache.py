# problem Statement

# You have cache which has get, set, clear and reconfigure method. reconfigure will call the clear internally
import threading

class ReconfigurableCache:
    def __init__(self, max_size=1000):
        self._cache = {}
        self._max_size = max_size
        self._lock = threading.RLock

    def get(self, key):
        with self._lock:
            return self._cache.get(key)
    
    def set(self, key, val):
        with self._lock:
            if len(self._cache) >= self._max_size:
                oldest_key = next(self._cache)
                del self._cache[oldest_key]

            self._cache[key] = val

    def clear(self):
        with self._lock:
            self._cache.clear()
    
    def reconfigure(self, new_size):
        with self._lock:
            self._max_size = new_size
            self.clear()

    