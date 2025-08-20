"""
Iterator is an object in python which enables you to traverse a container or a sequence of elements one by one. 
Two methods should be mandatory for this __iter__() and __next()__
__iter__(): it will return the object itself
__next()__: it will return the next item from the sequence, when there is no item it will raise StopIteration Exception

Every object you can iterate using for loop in python is an iterable

Conditions must follow to be an iterator:-
1. __iter__(): his method is called on the iterable object (e.g., a list). It must return an iterator object. In many cases, the object itself is the iterator, so it just returns self
2. __next__ method: This method is called on the iterator object. Each time it's called, it should return the next value in the sequence.
3. StopIteration exception: When the __next__() method is called and there are no more items to produce, it must raise a StopIteration exception. This is the signal that the for loop uses to stop iterating

"""

"""
How for loop is working internally:-
for loop is a high level abstraction that handles all the process and conditions of iternable.
When we write for item in my_list, python does following:-
1. it calls my_list.__iter()__ to get an iterator
2. it enters a loop, inside a loop it calls next iterator, which is equivalent to iterator.__next()__
3. it assign the return value to item
4. it continues this process unitl StopIteration is raised, at this point the loop terminates.
"""

# custom iterator:-

class CustomRangeIterator:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        self.current = start

    def __iter__(self):
        print("Inside __iter__ method")
        return self
    
    def __next__(self):
        print('Inside __next__ method')
        if self.current < self.end:
            number = self.current
            self.current += 1
            return number
        else:
            raise StopIteration
my_iter = CustomRangeIterator(1,3)       
try:
    print(f'Next iteration: {next(my_iter)}')
    print(f'Next iteration: {next(my_iter)}')
    print(f'Next iteration: {next(my_iter)}')
except StopIteration:
    print('got stop iteration call')


# with 4 loop
# here you are just calling class and for loop automatically calling __iter()__ and __next()__
for num in CustomRangeIterator(1, 5):
    print(num)



