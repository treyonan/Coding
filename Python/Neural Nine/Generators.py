import sys

# example 1

def mygenerator(n):
    for x in range(n):
        yield x ** 3

values = mygenerator(100)

print(next(values))
print(next(values))
print(next(values))
print(next(values))
print(f" size is {sys.getsizeof(values)}")

# example 2

def infinite_sequence():
    result = 1
    while True:
        yield result
        result *= 5

values = infinite_sequence()

print(next(values))
print(next(values))
print(next(values))
print(next(values))