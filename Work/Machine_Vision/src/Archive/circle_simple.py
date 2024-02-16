import cv2
import numpy as np
from collections import deque

# Callback function for trackbar
def nothing(x):
    pass

# Create a window for the trackbars
cv2.namedWindow('Settings')

# Create trackbars for parameter adjustment
cv2.createTrackbar('dp', 'Settings', 1, 10, nothing)
cv2.createTrackbar('minDist', 'Settings', 45, 100, nothing)
cv2.createTrackbar('param1', 'Settings', 65, 100, nothing)
cv2.createTrackbar('param2', 'Settings', 45, 100, nothing)
cv2.createTrackbar('minRadius', 'Settings', 0, 100, nothing)
cv2.createTrackbar('maxRadius', 'Settings', 0, 100, nothing)
cv2.createTrackbar('avgSamples', 'Settings', 10, 50, nothing)  # Adjust maximum value as needed

# Start video capture
cap = cv2.VideoCapture(1)

# Dictionary to store centroid positions for each circle
circle_centroids = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2, 2)

    dp = cv2.getTrackbarPos('dp', 'Settings')
    minDist = cv2.getTrackbarPos('minDist', 'Settings')
    param1 = cv2.getTrackbarPos('param1', 'Settings')
    param2 = cv2.getTrackbarPos('param2', 'Settings')
    minRadius = cv2.getTrackbarPos('minRadius', 'Settings')
    maxRadius = cv2.getTrackbarPos('maxRadius', 'Settings')
    avgSamples = cv2.getTrackbarPos('avgSamples', 'Settings')

    circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, dp, minDist,
                               param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for idx, (x, y, r) in enumerate(circles[0, :]):
            if idx not in circle_centroids:
                circle_centroids[idx] = deque(maxlen=avgSamples)
            circle_centroids[idx].append((x, y))
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)

    # After processing all circles in the frame, check if we can calculate averages
    for idx, centroids in circle_centroids.items():
        if len(centroids) == avgSamples:
            avg_x = int(np.mean([pos[0] for pos in centroids]))
            avg_y = int(np.mean([pos[1] for pos in centroids]))
            print(f"Circle {idx}: Average Centroid - X: {avg_x}, Y: {avg_y}")
            # Consider clearing or resetting the deque here if you only want to print once per N samples
            # circle_centroids[idx].clear()

    cv2.imshow('Detected Circles', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
