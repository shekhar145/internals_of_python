"""
meta class is class of class
it's a blueprint for creating classes, like class is a blueprint of object
The default metaclass in Python is type, we can create our own metaclass to customize class creation

"""

import time

class EnforceAPI(type):
    """
    A metaclass that enforces the presence of a _timestamp attribute
    and a log_message method on all classes it creates.
    """
    def __new__(cls, name, bases, dct):
        # dct is dictionary of the class's attributes and methods

        if '_timestamp' not in dct:
            raise TypeError('Class must define a timestamp attribute')
        
        if 'log_message' not in dct:
            raise TypeError('class must define a log_message method')
        
        return super().__new__(cls, name, bases, dct)

# correct class  
class MyLogger(metaclass=EnforceAPI):
    _timestamp = time.time()

    def log_message(self, message):
        print(f"[{self._timestamp}] {message}")



# Example of a class that will fail because it violates the rules
try:
    class BadLogger(metaclass=EnforceAPI):
        # Missing _timestamp and log_message
        pass
except TypeError as e:
    print(f"\nCaught Expected Error: {e}")
