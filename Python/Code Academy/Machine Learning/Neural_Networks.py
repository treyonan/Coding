# Perceptrons -----------------------------------------------------------------------------

# Training set --------------------------------------------

import codecademylib3_seaborn
import matplotlib.pyplot as plt
import random

def generate_training_set(num_points):
	x_coordinates = [random.randint(0, 50) for i in range(num_points)]
	y_coordinates = [random.randint(0, 50) for i in range(num_points)]
	training_set = dict()
	for x, y in zip(x_coordinates, y_coordinates):
		if x <= 45-y:
			training_set[(x,y)] = 1
		elif x > 45-y:
			training_set[(x,y)] = -1
	return training_set

training_set = generate_training_set(30)

x_plus = []
y_plus = []
x_minus = []
y_minus = []

for data in training_set:
	if training_set[data] == 1:
		x_plus.append(data[0])
		y_plus.append(data[1])
	elif training_set[data] == -1:
		x_minus.append(data[0])
		y_minus.append(data[1])
    
fig = plt.figure()
ax = plt.axes(xlim=(-25, 75), ylim=(-25, 75))

plt.scatter(x_plus, y_plus, marker = '+', c = 'green', s = 128, linewidth = 2)
plt.scatter(x_minus, y_minus, marker = '_', c = 'red', s = 128, linewidth = 2)

plt.title("Training Set")

plt.show()

# The Perceptron Algorithm -------------------------------------------

class Perceptron:
  def __init__(self, num_inputs=2, weights=[1,1]):
    self.num_inputs = num_inputs
    self.weights = weights
    
  def weighted_sum(self, inputs):
    weighted_sum = 0
    for i in range(self.num_inputs):
      weighted_sum += self.weights[i]*inputs[i]
    return weighted_sum
  
  def activation(self, weighted_sum):
    if weighted_sum >= 0:
      return 1
    if weighted_sum < 0:
      return -1
    
  def training(self, training_set):
    foundLine = False
    while not foundLine:
      total_error = 0
      for inputs in training_set:
        prediction = self.activation(self.weighted_sum(inputs))
        actual = training_set[inputs]
        error = actual - prediction
        total_error += abs(error)
        for i in range(self.num_inputs):
          self.weights[i] += error*inputs[i]
      if total_error == 0:
        foundLine = True
      
cool_perceptron = Perceptron()
small_training_set = {(0,3):1, (3,0):-1, (0,-3):-1, (-3,0):1}
cool_perceptron.training(small_training_set)
print(cool_perceptron.weights)

# Weighted Bias -----------------------------

lines = []

class Perceptron:
  def __init__(self, num_inputs=3, weights=[1,1,1]):
    self.num_inputs = num_inputs
    self.weights = weights

  def weighted_sum(self, inputs):
    weighted_sum = 0
    for i in range(self.num_inputs):
      weighted_sum += self.weights[i]*inputs[i]
    return weighted_sum

  def activation(self, weighted_sum):
    if weighted_sum >= 0:
      return 1
    if weighted_sum < 0:
      return -1

  def training(self, training_set):
    foundLine = False
    while not foundLine:
      total_error = 0
      for inputs in training_set:
        prediction = self.activation(self.weighted_sum(inputs))
        actual = training_set[inputs]
        error = actual - prediction
        total_error += abs(error)
        for i in range(self.num_inputs):
          self.weights[i] += error*inputs[i]

      slope = -self.weights[0]/self.weights[1]
      intercept = -self.weights[2]/self.weights[1]
      y1 = (slope * 0) + intercept
      y2 = (slope * 50) + intercept
      lines.append([[0,50], [y1, y2]])

      if total_error == 0:
        foundLine = True

# Data pre-processing for tensorflow ----------------------------------------------

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer

#load the dataset
dataset = pd.read_csv('insurance.csv') 
#choose first 7 columns as features
features = dataset.iloc[:,0:6] 
#choose the final column for prediction
labels = dataset.iloc[:,-1] 

#one-hot encoding for categorical variables
features = pd.get_dummies(features) 
#split the data into training and test data
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.33, random_state=42) 
 
#normalize the numeric columns using ColumnTransformer
ct = ColumnTransformer([('normalize', Normalizer(), ['age', 'bmi', 'children'])], remainder='passthrough')
#fit the normalizer to the training data and convert from numpy arrays to pandas frame
features_train_norm = ct.fit_transform(features_train) 
#applied the trained normalizer on the test data and convert from numpy arrays to pandas frame
features_test_norm = ct.transform(features_test) 

#ColumnTransformer returns numpy arrays. Convert the features to dataframes
features_train_norm = pd.DataFrame(features_train_norm, columns = features_train.columns)
features_test_norm = pd.DataFrame(features_test_norm, columns = features_test.columns)

# -----> your code here below
my_ct = ColumnTransformer([('scale', StandardScaler(), ['age', 'bmi', 'children'])], remainder='passthrough')
#fit the scaler to the training data and convert from numpy arrays to pandas frame
features_train_scale = my_ct.fit_transform(features_train) 
#applied the trained scaler on the test data and convert from numpy arrays to pandas frame
features_test_scale = my_ct.transform(features_test) 

#ColumnTransformer returns numpy arrays. Convert the features to dataframes
features_train_scale = pd.DataFrame(features_train_scale, columns = features_train.columns)
features_test_scale = pd.DataFrame(features_test_scale, columns = features_test.columns)

#print the summary statistics
print(features_train_scale.describe())
print(features_test_scale.describe())

# Neural network model: tf.keras.Sequential --------------------------------

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers


def design_model(features):
  model = Sequential()
  return model
  
dataset = pd.read_csv('insurance.csv') #load the dataset
features = dataset.iloc[:,0:6] #choose first 7 columns as features
labels = dataset.iloc[:,-1] #choose the final column for prediction

features = pd.get_dummies(features) #one-hot encoding for categorical variables
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.33, random_state=42) #split the data into training and test data
 
#standardize
ct = ColumnTransformer([('standardize', StandardScaler(), ['age', 'bmi', 'children'])], remainder='passthrough')
features_train = ct.fit_transform(features_train)
features_test = ct.transform(features_test)

#invoke the function for our model design
model = design_model(features_train)

#print the layers
print(model.layers)

# Neural network model: layers -------------------------------

import tensorflow as tf
from tensorflow.keras import layers
layer = layers.Dense(3) #3 is the number we chose

print(layer.weights) #we get empty weight and bias arrays because tensorflow doesn't know what the shape is of the input to this layer

# 1338 samples, 11 features as in our dataset
input = tf.ones((5000, 21)) 
# a fully-connected layer with 3 neurons
layer = layers.Dense(10) 
# calculate the outputs
output = layer(input) 
# print the weights
print(layer.weights) 

# Neural network model: input, output and hidden layers. Optimizers -----------------------------

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import InputLayer
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam


def design_model(features):
  model = Sequential(name = "my_first_model")
  input = InputLayer(input_shape=(features.shape[1],))
   #add an input layer
  model.add(input)
  #add a hidden layer with 128 neurons
  model.add(Dense(128, activation='relu')) 
  #add an output layer
  model.add(Dense(1)) 
  #your code here
  opt = Adam(learning_rate=0.01)
  model.compile(loss='mse',  metrics=['mae'], optimizer=opt)
  return model


dataset = pd.read_csv('insurance.csv') #load the dataset
features = dataset.iloc[:,0:6] #choose first 7 columns as features
labels = dataset.iloc[:,-1] #choose the final column for prediction

features = pd.get_dummies(features) #one-hot encoding for categorical variables
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.33, random_state=42) #split the data into training and test data
 
#standardize
ct = ColumnTransformer([('standardize', StandardScaler(), ['age', 'bmi', 'children'])], remainder='passthrough')
features_train = ct.fit_transform(features_train)
features_test = ct.transform(features_test)

#invoke the function for our model design
model = design_model(features_train)
print(model.summary())

# Training and evaluating the model -------------------------

mport pandas as pd
import tensorflow
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import InputLayer
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

tensorflow.random.set_seed(35) #for the reproducibility of results

def design_model(features):
  model = Sequential(name = "my_first_model")
  #without hard-coding
  input = InputLayer(input_shape=(features.shape[1],)) 
  #add the input layer
  model.add(input) 
  #add a hidden layer with 64 neurons
  model.add(Dense(128, activation='relu')) 
  #add an output layer to our model
  model.add(Dense(1)) 
  opt = Adam(learning_rate=0.1)
  model.compile(loss='mse',  metrics=['mae'], optimizer=opt)
  return model

dataset = pd.read_csv('insurance.csv') #load the dataset
features = dataset.iloc[:,0:6] #choose first 7 columns as features
labels = dataset.iloc[:,-1] #choose the final column for prediction

features = pd.get_dummies(features) #one-hot encoding for categorical variables
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.33, random_state=42) #split the data into training and test data
 
#standardize
ct = ColumnTransformer([('standardize', StandardScaler(), ['age', 'bmi', 'children'])], remainder='passthrough')
features_train = ct.fit_transform(features_train)
features_test = ct.transform(features_test)

#invoke the function for our model design
model = design_model(features_train)
print(model.summary())

#fit the model to the training data using 20 epochs, and 1 batch size
model.fit(features_train, labels_train, epochs = 40, batch_size = 1, verbose = 1)
 
#evaluate the model on the test data
val_mse, val_mae = model.evaluate(features_test, labels_test, verbose = 0)
 
print("MAE: ", val_mae)