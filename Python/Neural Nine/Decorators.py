import time

# example 1

def logged(function):
    def wrapper(*args, **kwargs):
        value = function(*args, **kwargs)
        with open('logfile.txt', 'a+') as f:
            fname = function.__name__
            print(f"{fname} returned value {value}")
            f.write(f"{fname} returned value {value}\n")
        return value
    return wrapper

@logged
def add(x, y):
    return x + y

print(add(10,20))

# example 2

def timed(function):
    def wrapper(*args, **kwargs):
        before = time.time()
        value = function(*args, **kwargs)
        after = time.time()
        fname = function.__name__
        print(f"{fname} took {after-before} seconds to execute")
        return value
    return wrapper

@timed
def myfunction(x):
    result = 1
    for i in range(1, x):
        result *= i
    return result

myfunction(10000)

# example 3

#decorator
def hello_decorator(func):
    #Wrapper function
    def inner1():
        print("Hello, this is before function execution")

        func()
        print("This is after function execution")
    
    return  inner1

# defining a function, to be called inside wrapper
def function_to_be_used():
    print("This is inside the function !!")

# pass 'function_to_be_used' inside the decorator to control its behavior
function_to_be_used = hello_decorator(function_to_be_used)

# calling the function
function_to_be_used()