from operator import ne


fruits = ["apple", "banana", "cherry", "kiwi", "mango"]

newlist = [x for x in fruits if "a" in x]

print(newlist)

newlist = [x for x in range(10)]

print(newlist)

newlist = [x.upper() for x in fruits]

print(newlist)

newlist = ['hello' for x in fruits]

print(newlist)

newlist = [x if x != "banana" else "orange" for x in fruits]

print(newlist)

matrix = [[j for j in range(3)] for i in range(5)]
  
print(matrix)