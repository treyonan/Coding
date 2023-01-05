# Creating a Set ----------------------

# Creating a set with curly braces
music_genres = {'country', 'punk', 'rap', 'techno', 'pop', 'latin'}

# Creating a set from a list using set()
music_genres_2 = set(['country', 'punk', 'rap', 'techno', 'pop', 'latin'])

# Set Comprehension -----------------------

items = ['country', 'punk', 'rap', 'techno', 'pop', 'latin']
 
music_genres = {category for category in items if category[0] == 'p'}
print(music_genres)

# Creating a Frozenset -------------------

frozen_music_genres = frozenset(['country', 'punk', 'rap', 'techno', 'pop', 'latin'])

empty_frozen_music_genres = frozenset()

# Adding to a Set ----------------------------------

song_tags = {'country', 'folk', 'acoustic'}
 
song_tags.add('guitar')
song_tags.add('country')
 
print(song_tags)

other_tags = ['live', 'blues', 'acoustic']
song_tags.update(other_tags)
 
print(song_tags)

# Removing From a Set -----------------------

song_tags = {'guitar', 'acoustic', 'folk', 'country', 'live', 'blues'}

song_tags.remove('folk')
print(song_tags)
 
# remove will throw an exception if key is not present 
song_tags.remove('fiddle')

# use discard to avoid exception
song_tags.discard('fiddle')
print(song_tags)

# Finding elements in a set -------------------

song_tags = {'guitar', 'acoustic', 'folk', 'country', 'live', 'blues'} 

print('country' in song_tags)

# Set Union --------------------- Includes A and B

prepare_to_py = {'rock', 'heavy metal', 'electric guitar', 'synth'}
 
py_and_dry = frozenset({'classic', 'rock', 'electric guitar', 'rock and roll'}) 

combined_tags = prepare_to_py.union(py_and_dry)
print(combined_tags)

frozen_combined_tags = py_and_dry | prepare_to_py
print(frozen_combined_tags)

# Set Intersection -------------------- Includes items common to both A and B

prepare_to_py = {'rock', 'heavy metal', 'electric guitar', 'synth'}
 
py_and_dry = frozenset({'classic', 'rock', 'electric guitar', 'rock and roll'}) 

frozen_intersected_tags = py_and_dry.intersection(prepare_to_py)
print(frozen_intersected_tags)

intersected_tags = prepare_to_py & py_and_dry
print(intersected_tags)

# Set Difference ---------------------------- Includes items in A that are NOT in B or common to B

prepare_to_py = {'rock', 'heavy metal', 'electric guitar', 'synth'}
 
py_and_dry = frozenset({'classic', 'rock', 'electric guitar', 'rock and roll'}) 

only_in_prepare_to_py = prepare_to_py.difference(py_and_dry)
print(only_in_prepare_to_py)

only_in_py_and_dry = py_and_dry - prepare_to_py
print(only_in_py_and_dry)

# Symmetric Difference -------------------------- Include all items from the sets which are in one or the other, but not both

prepare_to_py = {'rock', 'heavy metal', 'electric guitar', 'synth'}
 
py_and_dry = frozenset({'classic', 'rock', 'electric guitar', 'rock and roll'}) 

exclusive_tags = prepare_to_py.symmetric_difference(py_and_dry)
print(exclusive_tags)

frozen_exclusive_tags = py_and_dry ^ prepare_to_py
print(frozen_exclusive_tags)