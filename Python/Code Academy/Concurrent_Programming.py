# Introduction ---------------------------------------------------------------

import time
def sequential():
  s = time.perf_counter()
  print("Codecademy")
  time.sleep(2)
  print("says hello!")
  elapsed = time.perf_counter() - s
  print("Sequential Programming Elapsed Time: " + str(elapsed) + " seconds")

sequential()

# Multiple Threads --------------------------------------------------------

import time
import threading
def greeting_with_sleep(string):
  print(string)
  time.sleep(2)
  print("says hello!")


def main_threading():
  s = time.perf_counter()
  # your code goes here
  greetings = ['Codecademy', 'Chelsea', 'Hisham', 'Ashley']
  for i in range(len(greetings)):
    t = threading.Thread    (target=greeting_with_sleep, args=(greetings[i],))
    t.start()
  elapsed = time.perf_counter() - s
  print("Threading Elapsed Time: " + str(elapsed) + " seconds")

main_threading()

# Joining a Thread -----------------------------------------------------------------

import time
import threading
def greeting_with_sleep(string):
  print(string)
  time.sleep(2)
  print("says hello!")


def main_threading():
  s = time.perf_counter()
  threads = []
  greetings = ['Codecademy', 'Chelsea', 'Hisham', 'Ashley']
  for i in range(len(greetings)):
    t = threading.Thread    (target=greeting_with_sleep, args=(greetings[i],)) 
    t.start()
    # add append code here
    threads.append(t)
  # add join code here
  for t in threads:
    t.join()