sku_list = [7046538, 8289407, 9056375, 2308597]

# Write your code below:
print(dir(sku_list))

sku_iterator_object_one = sku_list.__iter__()
print(sku_iterator_object_one)

sku_iterator_object_two = iter(sku_list)
print(sku_iterator_object_two)

#-------------------------------------------------------------

dog_foods = {
  "Great Dane Foods": 4,
  "Min Pip Pup Foods": 10,
  "Pawsome Pup Foods": 8
}

# Write your code below:
dog_food_iterator = iter(dog_foods)


next(dog_food_iterator)
next_dog_food1 = next(dog_food_iterator)
print(next_dog_food1)
next_dog_food2 = next(dog_food_iterator)
#next_dog_food3 = next(dog_food_iterator)
#print(next_dog_food2)
#print(next_dog_food3)

# Custom Iterators 1 ---------------------------------------

class CustomerCounter:
# Write your code below:
  def __iter__(self):
    self.count = 0
    return self

  def __next__(self):    
    self.count += 1
    if self.count > 100:
      raise StopIteration
    return self.count        
    

customer_counter = CustomerCounter()

for a in customer_counter:
  print(a)


class FishInventory:
  def __init__(self, fishList):
      self.available_fish = fishList
 
  def __iter__(self):
    self.index = 0
    return self
 
  def __next__(self):
    if self.index < len(self.available_fish):
      fish_status = self.available_fish[self.index] + " is available!"
      self.index += 1
      return fish_status
    else:
      raise StopIteration

fish_list = FishInventory(['shad', 'bass', 'catfish'])

for a in fish_list:
    print(a)

# Itertools ---------------------------------------------------------

import itertools

max_capacity = 1000
num_bags = 0

for i in itertools.count(start=13.5, step=13.5):
  if i > max_capacity:
    break
  num_bags += 1

print(num_bags)


great_dane_foods = [2439176, 3174521, 3560031]
min_pin_pup_foods = [6821904, 3302083]
pawsome_pup_foods = [9664865]

# Write your code below: 
all_skus_iterator = itertools.chain(great_dane_foods, min_pin_pup_foods, pawsome_pup_foods)

for i in all_skus_iterator:
  print(i)


collars = ["Red-S","Red-M", "Blue-XS", "Green-L", "Green-XL", "Yellow-M"]

# Write your code below: 
collar_combo_iterator = itertools.combinations(collars, 3)

for i in collar_combo_iterator:
  print(i)

