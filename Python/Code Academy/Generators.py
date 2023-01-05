# Generator ------------------

def class_standing_generator():
  yield 'Freshman'
  yield 'Sophomore'
  yield 'Junior'
  yield 'Senior'

class_standings = class_standing_generator()

for a in class_standings:
  print(a)

  # next() and StopIteration ----------------------

def student_standing_generator():
  student_standings = ['Freshman','Senior', 'Junior', 'Freshman']
  # Write your code below:
  for a in student_standings:
    if a == 'Freshman':
      yield 500

standing_values = student_standing_generator()

print(next(standing_values))
print(next(standing_values))
print(next(standing_values))

# Generator Expressions -------------------------

a_generator = (i*i for i in range(4))

# Generator Methods: send() ---------------------------

def count_generator():
  while True:
    n = yield
    print(n)
 
my_generator = count_generator()
next(my_generator) # 1st Iteration Output: 
next(my_generator) # 2nd Iteration Output: None
my_generator.send(3) # 3rd Iteration Output: 3
next(my_generator) # 4th Iteration Output: None

# Generator Methods: throw() --------------------------

def generator():
  i = 0
  while True:
    yield i
    i += 1
 
my_generator = generator()
for item in my_generator:
    if item == 3:
        my_generator.throw(ValueError, "Bad value given")

# Generator Methods: close() --------------------------

def generator():
  i = 0
  while True:
    yield i
    i += 1
 
my_generator = generator()
next(my_generator)
next(my_generator)
my_generator.close()
next(my_generator) # raises StopGenerator exception

# Connecting Generators ----------------------

def cs_courses():
    yield 'Computer Science'
    yield 'Artificial Intelligence'
 
def art_courses():
    yield 'Intro to Art'
    yield 'Selecting Mediums'
 
 
def all_courses():
    yield from cs_courses()
    yield from art_courses()
 
combined_generator = all_courses()

# Generator Pipelines -------------------------

def number_generator():
  i = 0
  while True:
    yield i
    i += 1
 
def even_number_generator(numbers):
  for n in numbers:
    if n % 2 == 0:
      yield n
 
even_numbers = even_number_generator(number_generator())
 
for e in even_numbers:
  print(e)
  if e == 100:
    break

# Generator Project

def summa():
    yield 'Summa Cum Laude'

def magna():
    yield 'Magna Cum Laude' 

def cum_laude():
    yield 'Cum Laude'

def honors_generator(gpas):
  for gpa in gpas:
    if gpa > 3.9:
      yield from summa()
    elif gpa > 3.7:
      yield from magna()
    elif gpa > 3.5:
      yield from cum_laude()


def graduation_countdown(days):
  while days >= 0:
    days_left = yield days
    if days_left != None:
      days = days_left
    else:
      days -= 1


days = 25
countdown_generator = (day for day in range(days, -1,-1))
grad_days = graduation_countdown(days)
for day in grad_days:
  if day == 15:
    grad_days.send(10)
  elif day == 3:
    grad_days.close()
  print("Days Left: " + str(day))


days = 25
gpas = [3.2, 4.0, 3.6, 2.9]
honors = honors_generator(gpas)
for honor_label in honors:
  print(honor_label)
