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

