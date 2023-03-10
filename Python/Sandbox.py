import matplotlib.pyplot as plt
        
# Input data
x = [1000,4000,7000]
y = [396,1627,2867]


# Calculate the necessary values
n = len(x)
sum_x = sum(x)
sum_y = sum(y)
sum_xy = sum([x[i] * y[i] for i in range(n)])
sum_x_squared = sum([x[i] ** 2 for i in range(n)])

# Calculate the slope and y-intercept of the line of best fit
m = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x ** 2)
b = (sum_y - m * sum_x) / n

y2 = [i*m+b for i in x]

print(n)
print(sum_x)
print(sum_y)
print(sum_xy)
print(sum_x_squared)
print(m)
print(b)

for i in y2:
    print(i)

plt.plot(x,y,"o")

plt.plot(x, y2)

plt.show()