dict1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
# Double each value in the dictionary
double_dict1 = {k:v*2 for (k,v) in dict1.items()}
print(double_dict1)

numbers = range(10)
new_dict_comp = {n:n**2 for n in numbers if n%2 == 0}