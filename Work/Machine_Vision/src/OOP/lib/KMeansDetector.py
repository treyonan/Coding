from .CircleDetectionBase import CircleDetectionBase
import cv2
import numpy as np
from sklearn.cluster import KMeans

class KMeansCircleDetector(CircleDetectionBase):
    def __init__(self, num_clusters=3):
        super().__init__()
        self.num_clusters = num_clusters

    def process_centroids(self, frame, centroids):
        if centroids:
            centroids_array = np.array(centroids)
            if len(centroids_array) >= self.num_clusters:
                kmeans = KMeans(n_clusters=self.num_clusters, random_state=0).fit(centroids_array)
                for idx, center in enumerate(kmeans.cluster_centers_):
                    cv2.circle(frame, (int(center[0]), int(center[1])), 5, (0, 0, 255), -1)
                    print('k means')

