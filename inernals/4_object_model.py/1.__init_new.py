class MyClass:
    def __new__(cls, *args, **kwargs):
        print("1. __new__ is called to create the object.")
        # We must call the superclass's __new__ to get the actual object
        instance = super().__new__(cls)
        print("2. A new, empty instance has been created.")
        return instance

    def __init__(self, value):
        print("3. __init__ is called to initialize the instance.")
        self.value = value
        print(f"4. The instance's 'value' attribute is set to {self.value}.")

# Instantiating the class
obj = MyClass(100)
obj = MyClass(200)
print(f"\nFinal object value: {obj.value}")