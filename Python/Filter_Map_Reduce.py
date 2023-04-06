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