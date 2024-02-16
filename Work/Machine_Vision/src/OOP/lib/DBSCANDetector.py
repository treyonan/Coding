# DBSCANDetector.py
import cv2  # Make sure to import cv2 here
import numpy as np
from .CircleDetectionBase import CircleDetectionBase
from sklearn.cluster import DBSCAN

class DBSCANCircleDetector(CircleDetectionBase):
    def __init__(self, eps=10, min_samples=5):
        super().__init__()
        self.eps = eps
        self.min_samples = min_samples

    def cluster_and_draw(self, frame, centroids):
        if centroids:
            centroids_array = np.array(centroids)
            dbscan = DBSCAN(eps=self.eps, min_samples=self.min_samples).fit(centroids_array)
            labels = dbscan.labels_
            unique_labels = set(labels)
            for label in unique_labels:
                if label == -1:
                    continue  # Skip noise
                class_member_mask = (labels == label)
                xy = centroids_array[class_member_mask]
                centroid = np.mean(xy, axis=0)
                cv2.circle(frame, (int(centroid[0]), int(centroid[1])), 5, (0, 255, 255), -1)
                