"""
Iterator vs iterable

Iterable: Any obejct with a iter methodis an iterable
Iterator: Any object with next and iter method is iterator, Iterators are single use

Why Iterator are single use:-
An iterator is fundamentally a stateful object. It maintains its position within the sequence. 
Once the __next__() method has raised StopIteration, the iterator's state is "exhausted" and it cannot be rewound.
This is a critical design choice, as it directly ties into one of the biggest benefits of iterators: memory efficiency.


Why Iterator are memory efficient:-
his is the key reason iterators are so powerful. Instead of loading an entire sequence into memory at once, an iterator generates or fetches one item at a time, on demand.

Consider a scenario where you're processing a massive file or a huge data stream. If you were to load it all into a list, your program could crash due to memory overflow. An iterator allows you to process the data piece by piece.

For example, the range() function in Python doesn't create a list of a million numbers in memory. Instead, it returns an iterator that generates one number at a time when you ask for it.
"""
import sys

# This creates a list of 100,000 numbers in memory.
list_of_numbers = list(range(100000))
print(f"Size of list in memory: {sys.getsizeof(list_of_numbers)} bytes")
# Size of list in memory: 800064 bytes

# This creates an iterator object, which only stores its start, stop, and step values.
iterator_of_numbers = range(100000)
print(f"Size of iterator in memory: {sys.getsizeof(iterator_of_numbers)} bytes")
# Size of iterator in memory: 48 bytes