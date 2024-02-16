# Iterative example -----------------------------------------------------------------

def sum_to_one(n):
  result = 1
  call_stack = []
  
  while n != 1:
    execution_context = {"n_value": n}
    call_stack.append(execution_context)
    n -= 1
    print(call_stack)
  print("BASE CASE REACHED")
  
  while len(call_stack) != 0:
    return_value = call_stack.pop()
    print("Return value of {0} adding to result {1}".format(return_value['n_value'], result))
    result += return_value['n_value']
  return result, call_stack

sum_to_one(4)

# Recursion examples -----------------------------------------------------------------

# Define sum_to_one() below...
def sum_to_one(n):
  if n == 1:
    return n
  else:
    print("Recursing with input: {0}".format(n))
    return n + sum_to_one(n-1)


# uncomment when you're ready to test
print(sum_to_one(7))

# Factorial -------------------------------------------

def factorial(n):
  if n == 1:
    return n
  else:
    return n * factorial(n-1)
    
print(factorial(12))

# Power set ------------------------------------------

def power_set(my_list):
    # base case: an empty list
    if len(my_list) == 0:
        return [[]]
    # recursive step: subsets without first element
    power_set_without_first = power_set(my_list[1:])
    # subsets with first element
    with_first = [ [my_list[0]] + rest for rest in power_set_without_first ]
    # return combination of the two
    return with_first + power_set_without_first
  
universities = ['MIT', 'UCLA', 'Stanford', 'NYU']
power_set_of_universities = power_set(universities)

for set in power_set_of_universities:
  print(set)

# flatten ----------------------------------

def flatten(my_list):
  result = []
  for el in my_list:
    if isinstance(el, list):
      print("list found!")
      flat_list = flatten(el)
      result += flat_list
    else:
      result.append(el)
  return result


### reserve for testing...
planets = ['mercury', 'venus', ['earth'], 'mars', [['jupiter', 'saturn']], 'uranus', ['neptune', 'pluto']]
print(flatten(planets))

# fibonacci -------------------------------------

def fibonacci(n):
  # base cases
  if n == 1:
    return n
  if n == 0:
    return n
  
  # recursive step
  print("Recursive call with {0} as input".format(n))
  return fibonacci(n - 1) + fibonacci(n - 2)


fibonacci(5)
# set the appropriate runtime:
# 1, logN, N, N^2, 2^N, N!
fibonacci_runtime = "2^N"


# Recursive data structures -----------------------------------------------

def build_bst(my_list):
  if len(my_list) == 0:
    return "No Child"

  middle_idx = len(my_list) // 2
  middle_value = my_list[middle_idx]
  
  print("Middle index: {0}".format(middle_idx))
  print("Middle value: {0}".format(middle_value))
  
  tree_node = {"data": middle_value}
  tree_node["left_child"] = build_bst(my_list[ : middle_idx])
  tree_node["right_child"] = build_bst(my_list[middle_idx + 1 : ])

  return tree_node
  
sorted_list = [12, 13, 14, 15, 16]
binary_search_tree = build_bst(sorted_list)
print(binary_search_tree)

# fill in the runtime as a string
# 1, logN, N, N*logN, N^2, 2^N, N!
runtime = "N*logN"

# Recursion Vs. Iteration Examples ------------------------------------------------

# Iterative Factorial

def factorial(n):  
  if n < 0:
    return ValueError("Inputs 0 or greater only")
  result = 1
  while n != 0:
    result *= n
    n -= 1
  return result

# test cases
print(factorial(3) == 6)
print(factorial(0) == 1)
print(factorial(5) == 120)

# Iterative Fibonacci

def fibonacci(n):
  if n < 0:
    ValueError("Input 0 or greater only!")

  fibs = [0, 1]
  
  if n <= len(fibs) - 1:
    return fibs[n]

  while n > len(fibs) - 1:
    fibs.append(fibs[-1] + fibs[-2])
    
  return fibs[-1]

# test cases
print(fibonacci(3) == 2)
print(fibonacci(7) == 13)
print(fibonacci(0) == 0)
