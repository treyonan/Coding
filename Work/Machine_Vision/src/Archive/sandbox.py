import cv2
import numpy as np
from sklearn.cluster import DBSCAN

class CircleDetector:
    def __init__(self):
        self.init_trackbars()

    def init_trackbars(self):
        cv2.namedWindow('Settings')
        cv2.createTrackbar('dp', 'Settings', 1, 50, lambda x: None)
        cv2.createTrackbar('minDist', 'Settings', 200, 200, lambda x: None)
        cv2.createTrackbar('param1', 'Settings', 261, 300, lambda x: None)
        cv2.createTrackbar('param2', 'Settings', 40, 100, lambda x: None)
        cv2.createTrackbar('minRadius', 'Settings', 0, 100, lambda x: None)
        cv2.createTrackbar('maxRadius', 'Settings', 52, 200, lambda x: None)
        # DBSCAN parameters
        cv2.createTrackbar('eps', 'Settings', 10, 100, lambda x: None)  # Starting at 10 for eps, adjust as needed
        cv2.createTrackbar('min_samples', 'Settings', 10, 20, lambda x: None)  # Starting min_samples at 5
        cv2.createTrackbar('min_cluster_size', 'Settings', 2, 20, lambda x: None)  # Starting min_cluster_size at 3

    def detect_circles(self, frame):
        dp = cv2.getTrackbarPos('dp', 'Settings') / 10.0
        minDist = cv2.getTrackbarPos('minDist', 'Settings')
        param1 = cv2.getTrackbarPos('param1', 'Settings')
        param2 = cv2.getTrackbarPos('param2', 'Settings')
        minRadius = cv2.getTrackbarPos('minRadius', 'Settings')
        maxRadius = cv2.getTrackbarPos('maxRadius', 'Settings')
        # DBSCAN parameters from trackbars
        eps = cv2.getTrackbarPos('eps', 'Settings')
        min_samples = cv2.getTrackbarPos('min_samples', 'Settings')
        min_cluster_size = cv2.getTrackbarPos('min_cluster_size', 'Settings')
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_blurred = cv2.GaussianBlur(gray, (5, 5), 1.5)
        detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, dp, minDist,
                                            param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
        
        centroids = []
        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))
            for circle in detected_circles[0, :]:
                centroids.append([circle[0], circle[1]])
                
        return centroids, eps, min_samples, min_cluster_size

    def run(self):
        cap = cv2.VideoCapture(0)  # Use 0 for the default camera
        all_centroids = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            centroids, eps, min_samples, min_cluster_size = self.detect_circles(frame)
            all_centroids.extend(centroids)
            
            if len(all_centroids) > min_samples:
                centroids_array = np.array(all_centroids)
                dbscan = DBSCAN(eps=eps, min_samples=min_samples).fit(centroids_array)
                labels = dbscan.labels_

                # Drawing clusters based on DBSCAN results
                for k in set(labels):
                    if k == -1 or np.sum(labels == k) < min_cluster_size:  # Skip noise and small clusters
                        continue
                    class_member_mask = (labels == k)
                    xy = centroids_array[class_member_mask]
                    centroid = np.mean(xy, axis=0)
                    cv2.circle(frame, (int(centroid[0]), int(centroid[1])), 20, (0, 255, 0), 2)
                    cv2.circle(frame, (int(centroid[0]), int(centroid[1])), 2, (0, 0, 255), 3)
                
                all_centroids.clear()  # Clear centroids for the next round
            
            cv2.imshow('Frame with Detected Circles', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    detector = CircleDetector()
    detector.run()
