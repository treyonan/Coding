import cv2
import numpy as np
from collections import deque, defaultdict

class CircleDetector:
    def __init__(self):
        self.circle_centroids = {}
        self.circle_diameters = defaultdict(deque)  # Use diameters instead of radii
        self.avg_diameter = 0
        self.prev_avgSamples = 0  # Keep track of previous avgSamples to detect changes

        self.init_trackbars()

    def init_trackbars(self):
        cv2.namedWindow('Settings')
        cv2.createTrackbar('dp', 'Settings', 1, 10, lambda x: None)
        cv2.createTrackbar('minDist', 'Settings', 45, 100, lambda x: None)
        cv2.createTrackbar('param1', 'Settings', 65, 100, lambda x: None)
        cv2.createTrackbar('param2', 'Settings', 45, 100, lambda x: None)
        cv2.createTrackbar('minRadius', 'Settings', 0, 100, lambda x: None)
        cv2.createTrackbar('maxRadius', 'Settings', 0, 100, lambda x: None)
        cv2.createTrackbar('avgSamples', 'Settings', 1, 50, lambda x: None)

    def detect_circles(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2, 2)

        dp = cv2.getTrackbarPos('dp', 'Settings')
        minDist = cv2.getTrackbarPos('minDist', 'Settings')
        param1 = cv2.getTrackbarPos('param1', 'Settings')
        param2 = cv2.getTrackbarPos('param2', 'Settings')
        minRadius = cv2.getTrackbarPos('minRadius', 'Settings')
        maxRadius = cv2.getTrackbarPos('maxRadius', 'Settings')
        avgSamples = cv2.getTrackbarPos('avgSamples', 'Settings')

        # Check if avgSamples has changed, if so, recreate deques with new maxlen
        if avgSamples != self.prev_avgSamples:
            for key in self.circle_diameters.keys():
                self.circle_diameters[key] = deque([d * 2 for d in self.circle_diameters[key]], maxlen=avgSamples)
            self.prev_avgSamples = avgSamples

        circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, dp, minDist,
                                   param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            print(f"Circles detected in this frame: {len(circles[0, :])}")
            for i in circles[0, :]:
                diameter = i[2] * 2  # Calculate diameter
                self.circle_centroids.setdefault(i[0], deque(maxlen=avgSamples)).append((i[0], i[1]))
                self.circle_diameters.setdefault(i[0], deque(maxlen=avgSamples)).append(diameter)
                cv2.circle(frame, (i[0], i[1]), diameter // 2, (0, 255, 0), 2)  # Use diameter // 2 for radius
                cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)

        # Calculate average diameter for all circles in the current frame
        if any(self.circle_diameters.values()):
            all_diameters = [d for diameters in self.circle_diameters.values() for d in diameters]
            self.avg_diameter = int(np.mean(all_diameters)) if all_diameters else 0

        return self.avg_diameter

# Main code
detector = CircleDetector()

cap = cv2.VideoCapture(1)  # Adjust camera index if necessary

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    avg_diam = detector.detect_circles(frame)
    print(f"Average Diameter: {avg_diam}")

    cv2.imshow('Detected Shapes', frame) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
