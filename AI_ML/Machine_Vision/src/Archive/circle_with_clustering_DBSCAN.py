import cv2
import numpy as np
from sklearn.cluster import DBSCAN


class CircleDetector:
    def __init__(self, eps=10, min_samples=5):
        self.eps = eps
        self.min_samples = min_samples
        self.init_trackbars()

    def init_trackbars(self):
        cv2.namedWindow('Settings')
        cv2.createTrackbar('dp', 'Settings', 1, 50, lambda x: None)  # Scale for dp to allow float values
        cv2.setTrackbarMin('dp', 'Settings', 1)
        cv2.createTrackbar('minDist', 'Settings', 21, 200, lambda x: None)
        cv2.setTrackbarMin('minDist', 'Settings', 1)
        cv2.createTrackbar('param1', 'Settings', 35, 300, lambda x: None)
        cv2.setTrackbarMin('param1', 'Settings', 1)
        cv2.createTrackbar('param2', 'Settings', 41, 100, lambda x: None)
        cv2.setTrackbarMin('param2', 'Settings', 1)
        cv2.createTrackbar('minRadius', 'Settings', 0, 100, lambda x: None)
        cv2.setTrackbarMin('minRadius', 'Settings', 0)
        cv2.createTrackbar('maxRadius', 'Settings', 52, 200, lambda x: None)
        cv2.setTrackbarMin('maxRadius', 'Settings', 0)

    def detect_circles_and_draw(self, frame):
        dp = cv2.getTrackbarPos('dp', 'Settings') / 10.0
        minDist = cv2.getTrackbarPos('minDist', 'Settings')
        param1 = cv2.getTrackbarPos('param1', 'Settings')
        param2 = cv2.getTrackbarPos('param2', 'Settings')
        minRadius = cv2.getTrackbarPos('minRadius', 'Settings')
        maxRadius = cv2.getTrackbarPos('maxRadius', 'Settings')
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_blurred = cv2.GaussianBlur(gray, (5, 5), 1.5)
        detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, dp, minDist,
                                            param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))
            print(f"Circles detected in this frame: {len(detected_circles[0, :])}")
            for circle in detected_circles[0, :]:
                cv2.circle(frame, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
                cv2.circle(frame, (circle[0], circle[1]), 2, (0, 0, 255), 3)

    def run_detection(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            self.detect_circles_and_draw(frame)
            cv2.imshow('Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

def main():
    detector = CircleDetector(eps=10, min_samples=5)
    detector.run_detection()

if __name__ == "__main__":
    main()

    