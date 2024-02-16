import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

# Step 1: Load the saved model
model = tf.keras.models.load_model('C:/Python/Robot_Test_Machine_Vision/src/TensorFlow/circle_detector_model.h5')

# Step 2: Prepare the image
def prepare_image(img_path, target_size=(320, 569)):
    """
    Prepares an image for classification by the model.
    """
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)

# Example image path
img_path = 'C:/Python/Robot_Test_Machine_Vision/src/TensorFlow/classify/valve/valve_1.jpg'

# Prepare the image
prepared_image = prepare_image(img_path)

# Step 3: Classify the image
predictions = model.predict(prepared_image)

# Assuming a binary classification for simplicity, adjust based on your actual model
prediction = predictions[0][0]
class_label = 'Valve' if prediction > 0.5 else 'Not a valve'
print(f"Predicted class: {class_label} with score of {prediction}")

# If your model outputs class probabilities and you have more than two classes,
# you might want to use something like np.argmax(predictions) to get the index of the most likely class.
