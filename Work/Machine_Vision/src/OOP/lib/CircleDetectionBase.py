import cv2
import numpy as np

class CircleDetectionBase:
    def __init__(self):
        self.window_name = 'Settings'
        self.init_trackbars()

    def init_trackbars(self):
        cv2.namedWindow(self.window_name)
        cv2.createTrackbar('dp', self.window_name, 1, 50, lambda x: None)
        cv2.createTrackbar('minDist', self.window_name, 21, 200, lambda x: None)
        cv2.createTrackbar('param1', self.window_name, 35, 300, lambda x: None)
        cv2.createTrackbar('param2', self.window_name, 41, 100, lambda x: None)
        cv2.createTrackbar('minRadius', self.window_name, 0, 100, lambda x: None)
        cv2.createTrackbar('maxRadius', self.window_name, 52, 200, lambda x: None)
        cv2.createTrackbar('Y Threshold', self.window_name, 10, 100, lambda x: None)

    def detect_circles_and_draw(self, frame):
        dp = cv2.getTrackbarPos('dp', self.window_name) / 10.0
        minDist = cv2.getTrackbarPos('minDist', self.window_name)
        param1 = cv2.getTrackbarPos('param1', self.window_name)
        param2 = cv2.getTrackbarPos('param2', self.window_name)
        minRadius = cv2.getTrackbarPos('minRadius', self.window_name)
        maxRadius = cv2.getTrackbarPos('maxRadius', self.window_name)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_blurred = cv2.GaussianBlur(gray, (5, 5), 1.5)
        detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, dp, minDist,
                                            param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
        centroids = []
        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))
            for circle in detected_circles[0, :]:
                cv2.circle(frame, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
                cv2.circle(frame, (circle[0], circle[1]), 2, (0, 0, 255), 3)
                centroids.append([circle[0], circle[1]])
            #self.process_centroids(frame, centroids)

        return centroids

    def process_centroids(self, frame, centroids):
        # This method should be overridden by subclasses
        raise NotImplementedError("Subclass must implement abstract method")





