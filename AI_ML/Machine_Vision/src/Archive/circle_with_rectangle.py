import cv2
import numpy as np
from collections import deque, defaultdict

# Callback function for trackbar
def nothing(x):
    pass

# Initialize window and trackbars for settings
cv2.namedWindow('Settings')
cv2.createTrackbar('dp', 'Settings', 1, 10, nothing)  # Inverse ratio of the accumulator resolution for circles
cv2.createTrackbar('minDist', 'Settings', 45, 100, nothing)  # Minimum distance between detected circle centers
cv2.createTrackbar('param1', 'Settings', 65, 100, nothing)  # Upper threshold for the internal Canny edge detector for circles
cv2.createTrackbar('param2', 'Settings', 45, 100, nothing)  # Threshold for center detection in circle detection
cv2.createTrackbar('minRadius', 'Settings', 0, 100, nothing)  # Minimum circle radius
cv2.createTrackbar('maxRadius', 'Settings', 0, 100, nothing)  # Maximum circle radius
cv2.createTrackbar('avgSamples', 'Settings', 10, 50, nothing)  # Number of samples for averaging circle centroid positions

# Function to detect and process rectangles
def detect_rectangles(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 30, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) < 50:
            continue
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.03 * peri, True)
        if len(approx) == 4:
            cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            sorted_box = box[np.argsort(box[:, 0])]
            left_most = sorted_box[:2]
            right_most = sorted_box[2:]
            upper_left = left_most[np.argmin(left_most[:, 1])]
            lower_right = right_most[np.argmax(right_most[:, 1])]
            cv2.circle(frame, tuple(upper_left), 5, (0, 0, 255), -1)
            cv2.circle(frame, tuple(lower_right), 5, (0, 0, 255), -1)
            print(f"Rectangle - Upper Left: {tuple(upper_left)}, Lower Right: {tuple(lower_right)}")

# Function to detect and process circles
def detect_circles(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2, 2)
    dp = cv2.getTrackbarPos('dp', 'Settings')
    minDist = cv2.getTrackbarPos('minDist', 'Settings')
    param1 = cv2.getTrackbarPos('param1', 'Settings')
    param2 = cv2.getTrackbarPos('param2', 'Settings')
    minRadius = cv2.getTrackbarPos('minRadius', 'Settings')
    maxRadius = cv2.getTrackbarPos('maxRadius', 'Settings')
    avgSamples = cv2.getTrackbarPos('avgSamples', 'Settings')
    
    circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, dp, minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)


# Start video capture
cap = cv2.VideoCapture(1)  # Adjust camera index if necessary

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Circleeee detection
    detect_circles(frame)

    # Rectangle detection
    detect_rectangles(frame)

    cv2.imshow('Detected Shapes', frame)  # Show frame with both circles and rectangles detected

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
