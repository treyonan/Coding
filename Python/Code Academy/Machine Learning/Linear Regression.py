# Linear Regression ---------------------

import matplotlib.pyplot as plt

months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
revenue = [52, 74, 79, 95, 115, 110, 129, 126, 147, 146, 156, 184]

plt.plot(months, revenue, "o")

plt.title("Sandra's Lemonade Stand")

plt.xlabel("Months")
plt.ylabel("Revenue ($)")

#plt.show()

# Points and Lines --------------------------------

#slope:
m = 12
#intercept:
b = 40

y = [x*m+b for x in months]

plt.plot(months, y)

plt.show()

# Loss -------------------------------

x = [1, 2, 3]
y = [5, 1, 3]

#y = x
m1 = 1
b1 = 0

#y = 0.5x + 1
m2 = 0.5
b2 = 1

y_predicted1 = [i*m1+b1 for i in x]
y_predicted2 = [i*m2+b2 for i in x]

total_loss1 = 0

for i in range(len(y_predicted1)):
  total_loss1 += (y[i]-y_predicted1[i])**2

total_loss2 = 0

for i in range(len(y_predicted2)):
  total_loss2 += (y[i]-y_predicted2[i])**2

print(total_loss1)
print(total_loss2)

if total_loss1 < total_loss2:
  better_fit = 1
else:
  better_fit = 2

# Gradient Descent ---------------------------------

def get_gradient_at_b(x, y, m, b):
  return b