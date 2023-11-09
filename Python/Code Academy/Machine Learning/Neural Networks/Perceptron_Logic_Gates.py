import codecademylib3_seaborn
from sklearn.linear_model import Perceptron
import matplotlib.pyplot as plt
import numpy as np
from itertools import product

data = [[0,0],[0,1],[1,0],[1,1]]
labels = [0,0,0,1]

x = [point[0] for point in data]
y = [point[1] for point in data]

classifier = Perceptron(max_iter = 40, random_state = 22)
classifier.fit(data, labels)
score = classifier.score(data, labels)
print(score)
decision = classifier.decision_function([[0, 0], [1, 1], [0.5, 0.5]])
print(decision)
x_values = np.linspace(0, 1, 100)
y_values = np.linspace(0, 1, 100)
point_grid = list(product(x_values, y_values))
distances = classifier.decision_function(point_grid)
abs_distances = [abs(x) for x in distances]
distances_matrix = np.reshape(abs_distances, (100, 100))
heatmap = plt.pcolormesh(x_values, y_values, distances_matrix)
plt.colorbar(heatmap)
plt.show()







plt.scatter(x, y, c = labels)
plt.show()