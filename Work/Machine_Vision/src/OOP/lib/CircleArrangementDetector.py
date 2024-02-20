import numpy as np
from sklearn.cluster import DBSCAN
from collections import deque
from statistics import mode, StatisticsError

class CircleArrangementDetector:
    def __init__(self, eps=50, min_samples=1, sample_size=30):
        self.eps = eps
        self.min_samples = min_samples
        self.sample_size = sample_size        
        self.row_counts_history = []

    def update_and_aggregate_counts(self, detected_circles):
        if not detected_circles:
            # No circles detected in this frame
            return

        # Convert detected circles to a NumPy array for processing
        circle_positions = np.array(detected_circles)

        # Use DBSCAN to cluster circles into rows based on y-coordinate
        dbscan = DBSCAN(eps=self.eps, min_samples=self.min_samples, metric="euclidean")
        labels = dbscan.fit_predict(circle_positions[:, np.newaxis, 1])

        # Find unique row labels, excluding noise (-1)
        unique_rows = np.unique(labels[labels != -1])

        # Initialize or reset current frame counts
        current_frame_counts = [0] * len(unique_rows)

        # Count circles in each row based on labels
        for i, row_label in enumerate(unique_rows):
            current_frame_counts[i] = sum(labels == row_label)

        # Update row counts history, ensuring it's initialized
        while len(self.row_counts_history) < len(unique_rows):
            self.row_counts_history.append(deque(maxlen=self.sample_size))
        for i, count in enumerate(current_frame_counts):
            self.row_counts_history[i].append(count)

    def reset_counts_history(self):
        # Resets the history of counts for each row
        self.row_counts_history = []

    def get_most_common_counts(self):
        # Calculate the most common count for each row
        most_common_counts = []
        for row_history in self.row_counts_history:
            try:
                most_common_counts.append(mode(row_history))
            except StatisticsError:  # Handle cases without a single mode
                most_common_counts.append(max(set(row_history), key=row_history.count))  # Fallback strategy
        return most_common_counts
