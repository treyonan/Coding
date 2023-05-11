

nums = (16, 2, 19, 22, 10, 23, 16, 2, 27, 29, 19, 26, 12, 20, 16, 29, 6, 2, 12, 20)

# Checkpoint 1 code goes here.
filtered_numbers = filter(lambda x: x%2 ==0, nums)
print(tuple(filtered_numbers))

# Checkpoint 2 code goes here.
mapped_numbers = map(lambda x: x*3, nums)
print(tuple(mapped_numbers))

# Checkpoint 3 code goes here.
from functools import reduce
sum = reduce(lambda x,y: x+y, nums)
print(sum)

# Mapping a filtered collection ---------------------------------

nums = (2, 12, 5, 8, 9, 3, 16, 7, 13, 19, 21, 1, 15, 4, 22, 20, 11)

# Checkpoint 1 code goes here.
greater_than_10_doubled = map(lambda x: x*2, filter(lambda y: y>10,nums))
print(tuple(greater_than_10_doubled))

# Checkpoint 2 code goes here.
functional_way = map(lambda x: x*3, filter(lambda y: y%3==0, nums))
print(tuple(functional_way))

# Reducing a filtered collection --------------------

from collections import namedtuple
from functools import reduce

# Prices are in USD
menu_item = namedtuple("menu_item", ["name", "dish_type", "price"])

jsp = menu_item("Jumbo Shrimp Platter", "Appetizer", 29.95)
lc = menu_item("Lobster Cake", "Appetizer", 30.95)
scb = menu_item("Sizzling Canadian Bacon", "Appetizer", 9.95)
ccc = menu_item("Codecademy Crab Cake", "Appetizer", 32.95)
cs = menu_item("Caeser Salad", "Salad", 14.95)
mgs = menu_item("Mixed Green Salad", "Salad", 10.95)
cp = menu_item("Codecademy Potatoes", "Side", 34.95)
mp = menu_item("Mashed Potatoes", "Side", 14.95)
a = menu_item("Asparagus", "Side", 15.95)
rs = menu_item("Ribeye Steak", "Entree", 75.95)
phs = menu_item("Porter House Steak", "Entree", 131.95)
grs = menu_item("Grilled Salmon", "Entree", 36.95)

menu = (jsp, lc, scb, ccc, cs, mgs, cp, mp, a, rs, phs, grs)
entree = 0
least_expensive = 0

# Code for Checkpoint 1 goes here.
entree = reduce(lambda x,y: x if x.price > y.price else y, filter(lambda q: q.dish_type == "Entree", menu))

print(entree)

# Code for Checkpoint 2 goes here.
least_expensive = reduce(lambda x,y: x if x.price < y.price else y, filter(lambda q: q.dish_type == "Side" or q.dish_type == "Salad", menu))

print(least_expensive)

# Reducing a mapped collection --------------------

from functools import reduce

fruits = {"Grape":(4, 6, 2), "Lemon":(7, 3, 1), "Orange":(5, 8, 1), "Apple":(2, 8, 10), "Watermelon":(0, 9, 6)}

total_fruits = 0

total_fruits = reduce(lambda x, y: x + y, map(lambda q: fruits[q][0] + fruits[q][1] + fruits[q][2], fruits))

print(total_fruits)

# Combine all three higher order functions -------------

from functools import reduce

costs = {"shirt": (4, 13.00), "shoes":(2, 80.00), "pants":(3, 100.00), "socks":(5, 5.00), "ties":(3, 14.00), "watch":(1, 145.00)}

nums = (24, 6, 7, 16, 8, 2, 3, 11, 21, 20, 22, 23, 19, 12, 1, 4, 17, 9, 25, 15)

total = reduce(lambda x, y: x+y, filter(lambda r: r > 150.00, map(lambda q: costs[q][0] * costs[q][1], costs)))

print(total)

product = -1

product = reduce(lambda x, y: x * y, map(lambda z: z + 5, filter(lambda q: q < 10, nums)))

print(product)

# Working with CSV Files and Higher Order Functions ----------------------------------

import csv
from collections import namedtuple
from functools import reduce

tree = namedtuple("tree", ["index", "width", "height", "volume"]) 

with open('trees.csv', newline = '') as csvfile:
  reader = csv.reader(csvfile, delimiter=',', quotechar='|')
  next(reader)
  mapper = map(lambda x: tree(int(x[0].strip()), float(x[1]), int(x[2]), float(x[3])), reader)
  
  t = filter(lambda x: x.height > 75, mapper)
  trees = tuple(t)
  widest = reduce(lambda x, y: x if x.width > y.width else y, trees)
  print(widest)

  # Processing Data From JSON File ---------------------------------

  import json
from collections import namedtuple
from functools import reduce

city = namedtuple("city", ["name", "country", "coordinates", "continent"])

with open('cities.json') as json_file:
  data = json.load(json_file) 

cities = map(lambda x: city(x["name"], x["country"], x["coordinates"], x["continent"]), data["city"])

asia = tuple(filter(lambda x: x.continent == "Asia", cities))
print(asia)

west = None

west = reduce(lambda x, y: x if x.coordinates[1] < y.coordinates[1] else y, asia)

print(west)