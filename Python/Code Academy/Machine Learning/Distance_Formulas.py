# Euclidean Distance --------------------------------------

def euclidean_distance(pt1, pt2):
  distance = 0  
  for x in range(len(pt1)):
    distance += (pt1[x] - pt2[x])**2
  distance = distance ** 0.5
  return distance

print(euclidean_distance([1,2], [4,0]))
print(euclidean_distance([5,4,3], [1,7,9]))

# Manhattan Distance --------------------------------------

def manhattan_distance(pt1, pt2):
  distance = 0
  for i in range(len(pt1)):
    distance += abs(pt1[i] - pt2[i])
  return distance

print(manhattan_distance([1,2], [4,0]))
print(manhattan_distance([5,4,3], [1,7,9]))

# Hamming Distance ------------------------------

def hamming_distance(pt1, pt2):
  distance = 0
  for i in range(len(pt2)):
    if pt1[i] != pt2[i]:
      distance += 1
  return distance

print(hamming_distance([1,2], [1, 100]))
print(hamming_distance([5,4,9], [1,7,9]))

# SciPy Distances ----------------------------------

from scipy.spatial import distance

print(distance.euclidean([1,2], [4,0]))

print(distance.cityblock([1,2], [4,0]))

print(distance.hamming([5,4,9], [1,7,9]))