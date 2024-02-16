import cv2
import numpy as np
from collections import deque, defaultdict

# Callback function for trackbar
def nothing(x):
    pass

# Initialize window and trackbars for settings
cv2.namedWindow('Settings')
cv2.createTrackbar('dp', 'Settings', 1, 10, nothing)  # Inverse ratio of the accumulator resolution for circles
cv2.createTrackbar('minDist', 'Settings', 29, 100, nothing)  # Minimum distance between detected circle centers
cv2.createTrackbar('param1', 'Settings', 65, 100, nothing)  # Upper threshold for the internal Canny edge detector for circles
cv2.createTrackbar('param2', 'Settings', 46, 100, nothing)  # Threshold for center detection in circle detection
cv2.createTrackbar('minRadius', 'Settings', 0, 100, nothing)  # Minimum circle radius
cv2.createTrackbar('maxRadius', 'Settings', 0, 100, nothing)  # Maximum circle radius

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

    circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, dp, minDist,
                               param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)

    if circles is not None:
        global avg_diameter           
        circles = np.uint16(np.around(circles))
        num_circles = len(circles[0, :])     
        num_circles_samples.append(num_circles)   
        if len(num_circles_samples) == 10:
            # Calculate the maximum number of circles detected in the last 10 samples
            max_num_circles = max(num_circles_samples)
            print(f"Maximum circles detected in the last 10 frames: {max_num_circles}")
        
        # Calculate the average centroid and diameter for circles detected in the current frame
        avg_x = int(np.mean([x for x, y, _ in circles[0, :]]))
        avg_y = int(np.mean([y for x, y, _ in circles[0, :]]))
        avg_diameter = int(np.mean([2 * r for _, _, r in circles[0, :]]))
        
        #print(f"Frame's Average Centroid - X: {avg_x}, Y: {avg_y}, Diameter: {avg_diameter}")
        # Optional: Draw a circle or mark at the average centroid position for visualization
        #cv2.circle(frame, (avg_x, avg_y), 5, (255, 0, 0), -1)  # Draw the average centroid

        # Draw all detected circles
        for x, y, r in circles[0, :]:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)
    else:
        pass
        #print("No circles detected in this frame.")

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
num_circles_samples = deque(maxlen=10)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Circle detection
    avg_diam = detect_circles(frame)

    # Rectangle detection
    rect = detect_rectangles(frame)

    if rect and avg_diameter > 0:
        calculate_circles_in_rectangle(rect, avg_diameter)

    cv2.imshow('Detected Shapes', frame)  # Show frame with both circles and rectangles detected

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
