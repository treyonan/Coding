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
  print(string + " says hello!")

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

# Multiple Asynchronous Tasks ----------------------------------

import time
import asyncio

async def greeting_with_sleep_async(string):
  print(string)
  await asyncio.sleep(2)
  print(string + " says hello!")


async def main_async():
  s = time.perf_counter()
  greetings = [greeting_with_sleep_async('Codecademy'), greeting_with_sleep_async('Chelsea'), greeting_with_sleep_async('Hisham'), greeting_with_sleep_async('Ashley')]
  # your code goes here
  await asyncio.gather(*greetings)


  elapsed = time.perf_counter() - s
  print("Asyncio Elapsed Time: " + str(elapsed) + " seconds")

loop = asyncio.get_event_loop()
loop.run_until_complete(main_async())

# Multiprocessing ---------------------------------------

import time
import multiprocessing

def greeting_with_sleep(string):
  print(string)
  time.sleep(2)
  print(string + " says hello!")


def main_multiprocessing():
  s = time.perf_counter()
  processes = []
  greetings = ['Codecademy', 'Chelsea', 'Hisham', 'Ashley']
  # add your code here
  for i in range(len(greetings)):
    p = multiprocessing.Process(target=greeting_with_sleep, args=(greetings[i],))
    processes.append(p)
    p.start()

  for p in processes:
    p.join()
  
  elapsed = time.perf_counter() - s
  print("Multiprocessing Elapsed Time: " + str(elapsed) + " seconds")

main_multiprocessing()
