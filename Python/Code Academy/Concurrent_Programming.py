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

# The Threading Module --------------------------------------------------------

import time
import threading
def greeting_with_sleep(string):
  s = time.perf_counter()
  print(string)
  time.sleep(2)
  print("says hello!")
  elapsed = time.perf_counter() - s
  print("Sequential Programming Elapsed Time: " + str(elapsed) + " seconds")

greeting_with_sleep('Codecademy')

t = threading.Thread(target=greeting_with_sleep, args=('Codecademy',))
t.start()

