# Ordered Dict ------------------------------------------------------------------------

from collections import OrderedDict
 
orders = OrderedDict({'order_4829': {'type': 't-shirt', 'size': 'large', 'price': 9.99},
          'order_6184': {'type': 'pants', 'size': 'medium', 'price': 14.99},
          'order_2905': {'type': 'shoes', 'size': 12, 'price': 22.50}})
 
orders.move_to_end('order_4829')
orders.popitem()

# deque ----------------------------------------------------------

from collections import deque
 
bug_data = deque()
 
loaded_bug_reports = get_all_bug_reports()
 
for bug in loaded_bug_reports:
    if bug['priority'] == 'high':
        # With a deque, we can append to the front directly
        bug_data.appendleft(bug)
    else:
        bug_data.append(bug)
 
# With a deque, we can pop from the front directly
next_bug_to_fix = bug_data.popleft()

# Named Tuple -----------------------------------

from collections import namedtuple
 
# General Structure: namedtuple(typename, field_names, *, rename=False, defaults=None, module=None)
 
ActorData = namedtuple('ActorData', ['name', 'birth_year', 'movie', 'movie_release_date'])

actor_data = ActorData('Leonardo DiCaprio', 1974, 'Titanic', 1997)

print(actor_data.name)

clothes = [('t-shirt', 'green', 'large', 9.99),
           ('jeans', 'blue', 'medium', 14.99),
           ('jacket', 'black', 'x-large', 19.99),
           ('t-shirt', 'grey', 'small', 8.99),
           ('shoes', 'white', '12', 24.99),
           ('t-shirt', 'grey', 'small', 8.99)]

ClothingItem = namedtuple('ClothingItem', ['type', 'color', 'size', 'price'])

new_coat = ClothingItem('coat', 'black', 'small', 14.99)

coat_cost = new_coat.price

updated_clothes_data = []

for item in clothes:
  updated_clothes_data.append(ClothingItem(item[0], item[1], item[2], item[3]))

print(updated_clothes_data)

# DafaultDict -----------------------------------

from collections import defaultdict
 
validate_prices = defaultdict(lambda: 'No Price Assigned')

print(validate_prices['jacket'])

site_locations = {'t-shirt': 'Shirts',
                  'dress shirt': 'Shirts',
                  'flannel shirt': 'Shirts',
                  'sweatshirt': 'Shirts',
                  'jeans': 'Pants',
                  'dress pants': 'Pants',
                  'cropped pants': 'Pants',
                  'leggings': 'Pants'
                  }
updated_products = ['draped blouse', 'leggings', 'undershirt', 'dress shirt', 'jeans', 'sun dress', 'flannel shirt', 'cropped pants', 'dress pants', 't-shirt', 'camisole top', 'sweatshirt']

validated_locations = defaultdict(lambda: 'TODO: Add to website')

validated_locations.update(site_locations)

for a in updated_products:
  site_locations[a] = validated_locations[a]

print(site_locations)

# OrderedDict --------------------------------------------------------------

from collections import OrderedDict
 
orders = OrderedDict()

orders.update({'order_2905': {'type': 'shoes', 'size': 12, 'price': 22.50}})
orders.update({'order_6184': {'type': 'pants', 'size': 'medium', 'price': 14.99}})
orders.update({'order_4829': {'type': 't-shirt', 'size': 'large', 'price': 9.99}})

# Get a specific order
find_order = orders['order_2905']

# Get the data in a list format
orders_list = list(orders.items())
third_order = orders_list[2]

# Move an item to the end of the OrderedDict
orders.move_to_end('order_4829')
 
# Pop the last item in the dictionary
last_order = orders.popitem()

# The first 15 orders are provided
order_data = [['Order: 1', 'purchased'],
              ['Order: 2', 'purchased'],
              ['Order: 3', 'purchased'],
              ['Order: 4', 'returned'],
              ['Order: 5', 'purchased'],
              ['Order: 6', 'canceled'],
              ['Order: 7', 'returned'],
              ['Order: 8', 'purchased'],
              ['Order: 9', 'returned'],
              ['Order: 10', 'canceled'],
              ['Order: 11', 'purchased'],
              ['Order: 12', 'returned'],
              ['Order: 13', 'purchased'],
              ['Order: 14', 'canceled'],
              ['Order: 15', 'purchased']]

# Write your code below!
orders = OrderedDict(order_data)
to_move = []
to_remove = []

for key, val in orders.items():
  if val == 'returned':
    to_move.append(key)
  elif val == 'canceled':
    to_remove.append(key)

for item in to_remove:
  orders.pop(item)

for item in to_move:
  orders.move_to_end(item)

print(orders)

# ChainMap -----------------------------------------------------

from collections import ChainMap
 
customer_info = {'name': 'Dmitri Buyer', 'age': '31', 'address': '123 Python Lane', 'phone_number': '5552930183'}
 
shirt_dimensions = {'shoulder': 20, 'chest': 42, 'torso_length': 29}
 
pants_dimensions = {'waist': 36, 'leg_length': 42.5, 'hip': 21.5, 'thigh': 25, 'bottom': 18}

customer_data = ChainMap(customer_info, shirt_dimensions, pants_dimensions)

customer_leg_length = customer_data['leg_length']

customer_size_data = customer_data.parents

customer_data['address'] = '456 ChainMap Drive'

year_profit_data = [
    {'jan_profit': 15492.30, 'jan_holiday_profit': 2589.12},
    {'feb_profit': 17018.05, 'feb_holiday_profit': 3701.88},
    {'mar_profit': 11849.13},
    {'apr_profit': 9870.68},
    {'may_profit': 13662.34},
    {'jun_profit': 12903.54},
    {'jul_profit': 16965.08, 'jul_holiday_profit': 4360.21},
    {'aug_profit': 17685.69},
    {'sep_profit': 9815.57},
    {'oct_profit': 10318.28},
    {'nov_profit': 23295.43, 'nov_holiday_profit': 9896.55},
    {'dec_profit': 21920.19, 'dec_holiday_profit': 8060.79}
]

new_months_data = [
    {'jan_profit': 13977.85, 'jan_holiday_profit': 2176.43},
    {'feb_profit': 16692.15, 'feb_holiday_profit': 3239.74},
    {'mar_profit': 17524.35, 'mar_holiday_profit': 4301.92}
]

# Write your code below!

# Checkpoint #1
profit_map = ChainMap(*year_profit_data)

# Checkpoint #2
def get_profits(input_map):
    total_standard_profit = 0.0
    total_holiday_profit = 0.0

    for key in input_map.keys():
        if 'holiday' in key:
            total_holiday_profit += input_map[key]
        else:
            total_standard_profit += input_map[key]

    return total_standard_profit, total_holiday_profit

last_year_standard_profit, last_year_holiday_profit = get_profits(profit_map)

# Checkpoint #3
for item in new_months_data:
    profit_map = profit_map.new_child(item)

current_year_standard_profit, current_year_holiday_profit = get_profits(profit_map)

# Checkpoint #4
year_diff_standard_profit = current_year_standard_profit - last_year_standard_profit
year_diff_holiday_profit = current_year_holiday_profit - last_year_holiday_profit

print(year_diff_standard_profit)
print(year_diff_holiday_profit)

# Counter ---------------------------------------

from collections import Counter

clothes_list = ['skirt', 'hoodie', 'dress', 'blouse', 'jeans', 'shoes', 'skirt', 'skirt', 'jeans', 'hoodie', 'boots', 'jeans', 'jacket', 't-shirt', 'skirt', 'skirt', 'dress', 'shoes', 'blouse', 'hoodie', 'skirt', 'boots', 'shoes', 'boots', 'jeans', 'hoodie', 'blouse', 'hoodie', 'shoes', 'shoes', 'blouse', 'boots', 'blouse', 'hoodie', 't-shirt', 'jeans', 'dress', 'skirt', 'jacket', 'boots', 'skirt', 'dress', 'jeans', 'jeans', 'jacket', 'jeans', 'shoes', 'dress', 'hoodie', 'blouse']
 
counted_items = Counter(clothes_list)
print(counted_items)

opening_inventory = ['shoes', 'shoes', 'skirt', 'jeans', 'blouse', 'shoes', 't-shirt', 'dress', 'jeans', 'blouse', 'skirt', 'skirt', 'shorts', 'jeans', 'dress', 't-shirt', 'dress', 'blouse', 't-shirt', 'dress', 'dress', 'dress', 'jeans', 'dress', 'blouse']

closing_inventory = ['shoes', 'skirt', 'jeans', 'blouse', 'dress', 'skirt', 'shorts', 'jeans', 'dress', 'dress', 'jeans', 'dress', 'blouse']

def find_amount_sold(opening, closing, item):
  opening_count = Counter(opening)
  closing_count = Counter(closing)
  opening_count.subtract(closing_count)
  item = opening_count[item]
  return item

tshirts_sold = find_amount_sold(opening_inventory, closing_inventory, 't-shirt')

print(tshirts_sold)

# Container Wrappers ----------------------------------

class Customer:
 
  def __init__(self, name, age, address, phone_number):
    self.name = name
    self.age = age
    self.address = address
    self.phone_number = phone_number

class CustomerWrap(Customer):
 
  def __init__(self, name, age, address, phone_number):
    self.customer = Customer(name, age, address, phone_number)
 
  def display_customer_info(self):
    print('Name: ' + self.customer.name)
    print('Age: ' + str(self.customer.age))
    print('Address: ' + self.customer.address)
    print('Phone Number: ' + self.customer.phone_number)

customer = CustomerWrap('Dmitri Buyer', 38, '123 Python Avenue', '5557098603')
customer.display_customer_info()

# UserDict ------------------------------------------------------------

from collections import UserDict
 
# Create a class which inherits from the UserDict class
class DisplayDict(UserDict):
    # A new method to increase the dictionary's functionality
    def display_info(self):
        print("Number of Keys: " + str(len(self.keys())))
        print("Keys: " + str(list(self.keys())))
        print("Number of Values: " + str(len(self.values())))
        print("Values: " + str(list(self.values())))
 
    # We can also overwrite a method from the dictionary class
    def clear(self):
        print("Deleting all items from the dictionary!")
        super().clear()
 
disp_dict = DisplayDict({'user': 'Mark', 'device': 'desktop', 'num_visits': 37})
 
disp_dict.display_info()
 
disp_dict.clear()

data = {'order_4829': {'type': 't-shirt', 'size': 'large', 'price': 9.99, 'order_status': 'processing'},
        'order_6184': {'type': 'pants', 'size': 'medium', 'price': 14.99, 'order_status': 'complete'},
        'order_2905': {'type': 'shoes', 'size': 12, 'price': 22.50, 'order_status': 'complete'},
        'order_7378': {'type': 'jacket', 'size': 'large', 'price': 24.99, 'order_status': 'processing'}}


# Checkpoint #1
class OrderProcessingDict(UserDict):

    def clean_orders(self):
        to_del = []

        for key, val in self.data.items():
            if val['order_status'] == 'complete':
                to_del.append(key)

        for item in to_del:
            del self.data[item]

# Checkpoint #2
process_dict = OrderProcessingDict(data)
process_dict.clean_orders()
print(process_dict)

# UserList ----------------------------------------

from collections import UserList
 
# Create a class which inherits from the UserList class
class CondenseList(UserList):
 
    # A new method to remove duplicate items from the list
    def condense(self):
        self.data = list(set(self.data))
        print(self.data)
 
 
    # We can also overwrite a method from the list class
    def clear(self):
        print("Deleting all items from the list!")
        super().clear()
 
condense_list = CondenseList(['t-shirt', 'jeans', 'jeans', 't-shirt', 'shoes'])
 
condense_list.condense()
 
condense_list.clear()

data = [4, 6, 8, 9, 5, 7, 3, 1, 0]

class ListSorter(UserList):

  def append(self, item):
    super().append(item)
    super().sort()

sorted_list = ListSorter(data)
sorted_list.append(2)
print(sorted_list)

# UserString ---------------------------------------

from collections import UserString
 
# Create a class which inherits from the UserString class
class IntenseString(UserString):
 
    # A new method to capitalize and add exclamation points to our string
    def exclaim(self):
        self.data = self.data.upper() + '!!!'
        return self.data
 
 
    # Overwrite the count method to only count a certain letter
    def count(self, sub=None, start=0, end=0):
        num = 0
        for let in self.data:
            if let == 'P':
                num+=1
        return num
 
 
intense_string = IntenseString("python rules")
 
print(intense_string.exclaim())
print(intense_string.count())

str_name = 'python powered patterned products'
str_word = 'patterned '


# Checkpoint #1
class SubtractString(UserString):

    def __sub__(self, other):
        if other in self.data:
            self.data = self.data.replace(other, '')

# Checkpoint #2
subtract_string = SubtractString(str_name)
subtract_string - str_word
print(subtract_string)

# Collections Review --------------------------------------------------------------

overstock_items = [['shirt_103985', 15.99],
                    ['pants_906841', 19.99],
                    ['pants_765321', 15.99],
                    ['shoes_948059', 29.99],
                    ['shoes_356864', 9.99],
                    ['shirt_865327', 10.99],
                    ['shorts_086853', 9.99],
                    ['pants_267953', 21.99],
                    ['dress_976264', 32.99],
                    ['shoes_135786', 17.99],
                    ['skirt_196543', 12.99],
                    ['jacket_976535', 26.99],
                    ['pants_086367', 30.99],
                    ['dress_357896', 29.99],
                    ['shoes_157895', 14.99]]

# Write your code below!

# Checkpoint #1
split_prices = deque()

#Checkpoint #2
for item in overstock_items:
  if item[1] > 20.0:
    split_prices.appendleft(item)
  else:
    split_prices.append(item)
print(split_prices)

# Checkpoint #3
ClothesBundle = namedtuple('ClothesBundle', ['bundle_items', 'bundle_price'])

# Checkpoint #4
bundles = []
while len(split_prices) >= 5:
  bundle_list = [split_prices.pop(), split_prices.pop(), split_prices.pop(), split_prices.popleft(),split_prices.popleft()]

  calc_price = sum(b[1] for b in bundle_list)
  bundles.append(ClothesBundle(bundle_list, calc_price))

# Checkpoint #5
promoted_bundles = []
for bundle in bundles:
  if bundle.bundle_price > 100:
    promoted_bundles.append(bundle)

# # Checkpoint #6
print(promoted_bundles)

# for bundle in promoted_bundles:
#   print(bundle)  