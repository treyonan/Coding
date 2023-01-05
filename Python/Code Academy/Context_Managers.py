# With statement --------------------------------------------------------------

with open("file_name.txt", "w") as file:
   file.write("How you gonna win when you ain't right within?")

# Same as 

file = open("file_name.txt", "w")
try:
   file.write("How you gonna win when you ain't right within?")
finally:
   file.close()

# Class Based Context Managers -----------------------------------------

class PoemFiles:
  def __init__(self):
    print('Creating Poems!')

  def __enter__(self):
    print('Opening poem file')

  def __exit__(self, *exc):
    print('Closing poem file')

with PoemFiles() as manager:
  print('Hope is the thing with feathers')

# Class Based Context Managers II ---------------------------------------

class WorkWithFile:
  def __init__(self, file, mode):
    self.file = file
    self.mode = mode
 
  def __enter__(self):
    self.opened_file = open(self.file, self.mode)
    return self.opened_file
 
  def __exit__(self, *exc):
    self.opened_file.close()


with WorkWithFile("file.txt", "r") as file:
  print(file.read())

# example

class PoemFiles:
  def __init__(self, poem_file, mode):
    print('Starting up a poem context manager')
    self.file = poem_file
    self.mode = mode

  def __enter__(self):
    print('Opening poem file')
    self.opened_poem_file = open(self.file, self.mode)
    return self.opened_poem_file

  def __exit__(self, *exc):
    print('Closing poem file')
    self.opened_poem_file.close()


with PoemFiles('poem.txt', 'w') as open_poem_file:
  print('doing the thang')
  open_poem_file.write('Hope is the thing with feathers')

# Handling Exceptions I ----------------------------------------------

class OpenFile:
 
 def __init__(self, file, mode):
   self.file = file
   self.mode = mode
 
 def __enter__(self):
   self.opened_file = open(self.file, self.mode)
   return self.opened_file
 
 def __exit__(self, exc_type, exc_val, traceback):
   print(exc_type)
   print(exc_val)
   print(traceback)
   self.opened_file.close()

with OpenFile("file.txt", "r") as file:
  # .see() is not a real method
  print(file.see())

# Handling Exceptions II -----------------------------------

class OpenFile:
 
 def __init__(self, file, mode):
   self.file = file
   self.mode = mode
 
 def __enter__(self):
   self.opened_file = open(self.file, self.mode)
   return self.opened_file
 
 def __exit__(self, exc_type, exc_val, traceback):
   print(exc_type, exc_val, traceback)
   print("The exception has been handled")
   self.file.close()
   return True      # returning true will supporess any errors

with OpenFile("file.txt", "r") as file:
 # .see is not a real method
 print(file.see())
 
with OpenFile("file.txt", "r") as file:
 print(file.read())

# choose to handle a specific exception

class OpenFile:
 
 def __init__(self, file, mode):
   self.file = file
   self.mode = mode
 
 def __enter__(self):
   self.opened_file = open(self.file, self.mode)
   return self.opened_file
 
 def __exit__(self, exc_type, exc_val, traceback):
 
   if isinstance(exc_val, TypeError):
      # Handle TypeError here...
      print("The exception has been handled")
      return True
 
   self.file.close()

# Contextlib --------------------------------------------------

from contextlib import contextmanager

@contextmanager
def open_file_contextlib(file, mode):
  opened_file = open(file, mode)
 try:
   yield opened_file
 finally:
   opened_file.close()

with open_file_contextlib('file.txt', 'w') as opened_file:
 opened_file.write('We just made a context manager using contexlib')

 # Contextlib Error Handling -------------------------------------------- 
 
@contextmanager
def open_file_contextlib(file, mode):
  open_file = open(file, mode)
 
try:
   yield open_file
 
 # Exception Handling
 except Exception as exception:
   print('We hit an error: ' + str(exception))
 
 finally:
   open_file.close()
 
with open_file_contextlib('file.txt', 'w') as opened_file:
 opened_file.sign('We just made a context manager using contexlib')

 # example for a specific exception type

@contextmanager
def poem_files(file, mode):
  print('Opening File')
  open_poem_file = open(file, mode)
  try:
    yield open_poem_file  
  except AttributeError as e:
    print(e)
  finally:
    print('Closing File')
    open_poem_file.close()

with poem_files('poem.txt', 'a') as opened_file:
  print('Inside yield')
  opened_file.sign('Buzz is big city. big city is buzz.')

# Nested Context Managers ------------------------------------------

@contextmanager
def poem_files(file, mode):
  print('Opening File')
  open_poem_file = open(file, mode)
  try:
    yield open_poem_file
  finally:
    print('Closing File')
    open_poem_file.close()


@contextmanager
def card_files(file, mode):
  print('Opening File')
  open_card_file = open(file, mode)
  try:
    yield open_card_file
  finally:
    print('Closing File')
    open_card_file.close()

with poem_files('poem.txt', 'r') as poem:
  with card_files('card.txt', 'w') as card:
    print(poem, card)
    card.write(poem.read())



