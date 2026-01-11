import cv2
import numpy as np
from sklearn.cluster import KMeans

class CircleDetector:
    def __init__(self, num_clusters=3):
        self.num_clusters = num_clusters
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
        centroids = []
        if detected_circles is not None:            
            detected_circles = np.uint16(np.around(detected_circles))
            print(f"Circles detected in this frame: {len(detected_circles[0, :])}")
            for circle in detected_circles[0, :]:
                cv2.circle(frame, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
                cv2.circle(frame, (circle[0], circle[1]), 2, (0, 0, 255), 3)
                centroids.append([circle[0], circle[1]])        
        return centroids

    def run_detection(self):
        cap = cv2.VideoCapture(0)  # Use 0 for the default camera
        all_centroids = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            centroids = self.detect_circles_and_draw(frame)
            all_centroids.extend(centroids)
            
            cv2.imshow('Frame with Detected Circles', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

        if all_centroids:
            all_centroids_array = np.array(all_centroids)
            if len(all_centroids_array) >= self.num_clusters:
                kmeans = KMeans(n_clusters=self.num_clusters, random_state=0).fit(all_centroids_array)
                consistent_centroids = kmeans.cluster_centers_
                print("Most consistent centroid locations:", consistent_centroids)
            else:
                print("Not enough centroids for clustering.")

def main():
    detector = CircleDetector(num_clusters=3)
    detector.run_detection()


if __name__ == "__main__":
    main()
