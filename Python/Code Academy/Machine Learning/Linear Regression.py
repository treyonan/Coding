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

def get_gradient_at_b(x, y, b, m):
  N = len(x)
  diff = 0
  for i in range(N):
    x_val = x[i]
    y_val = y[i]
    diff += (y_val - ((m * x_val) + b))
  b_gradient = -(2/N) * diff  
  return b_gradient

def get_gradient_at_m(x, y, b, m):
  N = len(x)
  diff = 0
  for i in range(N):
      x_val = x[i]
      y_val = y[i]
      diff += x_val * (y_val - ((m * x_val) + b))
  m_gradient = -(2/N) * diff  
  return m_gradient

# Define your step_gradient function here
def step_gradient(x, y, b_current, m_current):
  b_gradient = get_gradient_at_b(x, y, b_current, m_current)
  m_gradient = get_gradient_at_m(x, y, b_current, m_current)  
  b = b_current - (0.01 * b_gradient)
  m = m_current - (0.01 * m_gradient)
  return b, m

months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
revenue = [52, 74, 79, 95, 115, 110, 129, 126, 147, 146, 156, 184]

# current intercept guess:
b = 0
# current slope guess:
m = 0

# Call your function here to update b and m
b, m = step_gradient(months, revenue, b, m)
print(b, m)









