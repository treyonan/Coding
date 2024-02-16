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
cv2.createTrackbar('avgSamples', 'Settings', 1, 50, nothing)  # Number of samples for averaging circle centroid positions

# Function to detect and process rectangles
def detect_rectangles(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 30, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    global rectangle

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
            #print(f"Rectangle - Upper Left: {tuple(upper_left)}, Lower Right: {tuple(lower_right)}")
        rectangle = cv2.minAreaRect(contour) 
    return rectangle

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

    circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, dp, minDist,
                               param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        print(f"Circles detected in this frame: {len(circles[0, :])}")
        for idx, (x, y, r) in enumerate(circles[0, :]):
            if idx not in circle_centroids:
                circle_centroids[idx] = deque(maxlen=avgSamples)
                circle_radii[idx] = deque(maxlen=avgSamples)
            circle_centroids[idx].append((x, y))
            circle_radii[idx].append(r)
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)
        
    # After processing all circles in the frame, check if we can calculate averages
    for idx, centroids in circle_centroids.items():
        if len(centroids) == avgSamples:
            avg_x = int(np.mean([pos[0] for pos in centroids]))
            avg_y = int(np.mean([pos[1] for pos in centroids]))
            global avg_diameter
            if idx in circle_radii and len(circle_radii[idx]) == avgSamples:
                avg_diameter = int(np.mean([2 * r for r in circle_radii[idx]]))  # Correct calculation of avg_diameter
                #print(f"Circle {idx}: Average Centroid - X: {avg_x}, Y: {avg_y}, Diameter: {avg_diameter}")
            else:
                avg_diameter = avg_diameter    
    return avg_diameter
    
def calculate_circles_in_rectangle(rect, avg_diam):
    # rect is the cv2.minAreaRect result, which includes ((center_x, center_y), (width, height), angle)
    _, (width, height), _ = rect
    
    # Calculate how many circles fit along the width and height
    circles_along_x = int(width // avg_diam)
    circles_along_y = int(height // avg_diam)
    
    #print(f"Circles along X: {circles_along_x}, Circles along Y: {circles_along_y}")

# Start video capture
cap = cv2.VideoCapture(1)  # Adjust camera index if necessary

# Dictionary to store centroid positions for each circle
circle_centroids = {}
circle_radii = defaultdict(lambda: deque(maxlen=avgSamples)) 
avg_diameter = 0
rectangle = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Circle detection
    avg_diam = detect_circles(frame)

    # Rectangle detection
    #rect = detect_rectangles(frame)

    #if rect and avg_diameter > 0:
    #    calculate_circles_in_rectangle(rect, avg_diameter)

    cv2.imshow('Detected Shapes', frame)  # Show frame with both circles and rectangles detected

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
