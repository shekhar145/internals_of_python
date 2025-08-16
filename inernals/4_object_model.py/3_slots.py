"""
How __slots__ Works
By default, every instance of a class in Python has a __dict__ dictionary to store its attributes. This is convenient and flexible because you can add new attributes to an object at runtime. However, a __dict__ consumes a significant amount of memory, especially if you create a large number of objects (e.g., millions of objects in a data processing pipeline).

The __slots__ attribute is a way to tell Python not to create an instance dictionary for objects of that class. Instead of a __dict__, __slots__ defines a fixed set of attributes that the instances can have. This saves memory because it pre-allocates a small amount of space for each attribute directly on the object itself, similar to a C struct, bypassing the overhead of a Python dictionary.

Key Benefits:

Memory Savings: This is the primary reason to use __slots__. It can lead to a 2x-3x reduction in memory consumption per object.

Faster Attribute Access: Accessing attributes can be slightly faster because the interpreter doesn't have to perform a dictionary lookup; it can access the attribute directly from its fixed offset.

Drawbacks:

You cannot add new attributes at runtime. You can only assign values to the attributes specified in __slots__.

Classes using __slots__ cannot have a __dict__. This can affect some methods or libraries that expect a __dict__ to exist.

Inheritance can be complex. A subclass without __slots__ will still have a __dict__. To get the memory-saving benefits, all classes in the inheritance chain must define __slots__.

"""

# Example how we can bypass dict and add slot

class SlottedObjectSimulator:
    #  This is the equivalent of __slots__ in our simplified model.
    # It defines the fixed set of attributes and their order.
    _slot_names = ('name', 'age', 'city')

    def __init__(self, name, age, city):
        # We store the values in a tuple, which simulates a fixed-size
        # C structure in memory.
        self._values = (name, age, city)

    def __getattr__(self, name):
        """
        This method is called for attribute lookups.
        We'll use it to simulate direct attribute access based on index.
        """
        try:
            index = self._slot_names.index(name)
            return self._values[index]
        except ValueError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        
    def __setattr__(self, name, value):
        """
        This method is called to set an attribute. We'll use it to simulate
        setting values at a fixed index.
        """
        if name == '_values':
            # This is a special case to allow the __init__ method to work
            object.__setattr__(self, name, value)
            return
            
        try:
            # Find the index for the attribute
            index = self._slot_names.index(name)
            
            # Create a new tuple with the updated value.
            # This simulates updating a value at a fixed memory offset.
            values_list = list(self._values)
            values_list[index] = value
            self._values = tuple(values_list)

        except ValueError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        

if __name__ == "__main__":
    p = SlottedObjectSimulator("Alice", 30, "New York")

    print(f"Name: {p.name}")
    print(f"Age: {p.age}")

    # You can't add a new attribute
    try:
        p.country = "USA"
    except AttributeError as e:
        print(f"\nCaught Expected Error: {e}")

    # You can change an existing attribute
    p.age = 31
    print(f"\nUpdated Age: {p.age}")
    
    # Check memory consumption (This is conceptual)
    import sys
    # A real object with __slots__ would be much smaller than this tuple-based simulation
    # but the principle is the same: fixed-size data structure vs. a dictionary.
    print(f"\nMemory size of the object: {sys.getsizeof(p)}")