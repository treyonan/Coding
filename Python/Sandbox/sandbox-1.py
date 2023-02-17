import cv2
import numpy as np

# Define a function to handle trackbar events
def on_trackbar(val):
    # Update the image with a color based on the trackbar position
    img[:] = (0, val, 255 - val)

    # Display the updated image
    cv2.imshow('image', img)

# Create a black image with three channels
img = np.zeros((512, 512, 3), np.uint8)

# Create a window to display the image
cv2.namedWindow('image')

# Create a trackbar with a range of 0-255 and an initial value of 0
cv2.createTrackbar('R', 'image', 0, 255, on_trackbar)

# Show the initial image
cv2.imshow('image', img)

# Wait for a key event
cv2.waitKey(0)

# Destroy all windows
cv2.destroyAllWindows()