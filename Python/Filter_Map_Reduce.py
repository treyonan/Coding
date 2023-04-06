# Filter ---------------------------------------------------

nums = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
 
filtered_numbers = filter(lambda x: x % 2 == 0, nums) 
 
print(tuple(filtered_numbers))
 
# This will output the tuple: (2, 4, 6, 8, 10)

# Map ----------------------------------------------------

numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
 
mapped_numbers = map(lambda x: x*x, numbers) 
 
print(tuple(mapped_numbers))
 
# This will also output: (1, 4, 9, 16, 25, 36, 49, 64, 81, 100)

# Reduce ---------------------------------------------------------

from functools import reduce
sum = reduce(lambda x,y: x+y, nums)
print(sum)

# Mapping a Filtered Collection ---------------------------------------------------

from collections import namedtuple
 
# Create a class called student
student = namedtuple("student", ["name", "grade", "course_number"]) 

# Create the records for the students in the form of tuples
 
peter = student("Peter", 'B', 101)
amanda = student("Amanda", 'C', 101 )
sarah = student("Sarah", 'A', 102)
lisa = student("Lisa", 'D', 101)
alex = student("Alex", 'A', 102)
maria = student("Maria", 'B', 101)
andrew = student("Andrew", 'C', 102)
 
math_class = (peter, amanda, sarah, lisa, alex, maria, andrew)

math_201 = map(lambda s: student(s.name, 'X', 201), filter(lambda q: q.grade <= 'B', math_class))
 
print(tuple(math_201))

# Reducing a filtered collection ----------------------------------------------------------

from collections import namedtuple
from functools import reduce
 
# Prices are in USD
menu_item = namedtuple("menu_item", ["name", "dish_type", "price"])
 
jsp = menu_item("Jumbo Shrimp Platter", "Appetizer", 29.95)
lc = menu_item("Lobster Cake", "Appetizer", 30.95)
scb = menu_item("Sizzling Canadian Bacon", "Appetizer", 9.95)
ccc = menu_item("Codecademy Crab Cake", "Appetizer", 32.95)
cs = menu_item("Caeser Salad", "Salad", 14.95)
mgs = menu_item("Mixed Green Salad", "Salad", 11.95)
cp = menu_item("Codecademy Potatoes", "Side", 34.95)
mp = menu_item("Mashed Potatoes", "Side", 14.95)
rs = menu_item("Ribeye Steak", "Entree", 75.95)
phs = menu_item("Porter House Steak", "Entree", 131.95)
 
menu = (jsp, lc, scb, ccc, cs, mgs, cp, mp, rs, phs)

# Imperative Solution

# apps only contains items with dish_type == "Appetizer"
apps = [i for i in menu if i.dish_type == "Appetizer"] 
cheapest_app = app[0] 
for i in apps:
  if i.price < cheapest_app.price:
    cheapest_app = i
 
print(cheapest_app) # Output will be: menu_item("Sizzling Canadian Bacon", "Appetizer", 9.95)

# Declarative Solution

cheapest_app = reduce(lambda x, y: x if x.price < y.price else y, filter(lambda x: x.dish_type == "Appetizer", menu))
 
print(cheapest_app) # Output will be: menu_item("Sizzling Canadian Bacon", "Appetizer", 9.95)

# Reducing a Mapped Collection -----------------------------------------------------------------

# Dictionary entry: {"name: (number_or_units_sold, price_per_unit_GBP)}
costs = {"shirt": (4, 13.00), "shoes":(2, 80.00), "pants":(3, 100.00), "socks":(5, 5.00)}
 
k = reduce(lambda x, y: x+y, map(lambda q: costs[q][0] * costs[q][1], costs))
print(k) # Output will be a total cost of: 537.0 GBP



fruits = {"Grape":(4, 6, 2), "Lemon":(7, 3, 1), "Orange":(5, 8, 1), "Apple":(2, 8, 10), "Watermelon":(0, 9, 6)}

total_fruits = 0

total_fruits = reduce(lambda x, y: x + y, map(lambda q: fruits[q][0] + fruits[q][1] + fruits[q][2], fruits))

print(total_fruits)