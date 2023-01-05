# multi thread example

import threading

def function1():
    for x in range (50):
        print("ONE")


def function2():
    for x in range(50):
        print("TWO")

def helloworld():
    for x in range(50):
        print("Hello World!")

t1 = threading.Thread(target=function1)
t2 = threading.Thread(target=function2)
t3 = threading.Thread(target=helloworld)

t1.start()
t2.start()
t3.start()

t3.join()

print("End of program")