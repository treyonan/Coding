check_if_A_grade = lambda grade: 'Got an A!' if grade >= 90 else 'Did not get an A.'

print(check_if_A_grade(50))



def times3(a, b, function):
  return 3 * function(a, b)
 
add_then_times3 = times3(2, 4, lambda x, y: x + y) # 18
sub_then_times3 = times3(2, 4, lambda x, y: x - y) # -6



def odd_or_even(n, even_function, odd_function):
  if n % 2 == 0:
    return even_function(n)
  else: 
    return odd_function(n) 

square = lambda x: x*x
cube = lambda x: x*x*x

test  = odd_or_even(3, square, cube)

print(test) 