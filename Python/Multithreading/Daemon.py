import threading
import time

path = "C:\Users\Trey\OneDrive\Documents\Trey\Projects\Coding\VS Code\Example Code\Multithreading\Text"
text = ""

def readFile():
    global path, text
    while True:
        with open(path, "r") as f:
            text = f.read()
        time.sleep(3)

def printloop():
    for x in range(30):
        print(text)
        time.sleep(1)

t1 = threading.Thread(target=readFile, daemon=True)
t2 = threading.Thread(target=printloop)

t1.start()
t2.start()

# added from work computer