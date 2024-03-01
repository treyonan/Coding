from statistics import mode, StatisticsError
import numpy as np

class DetectionsSmoothing:
    def __init__(self, N):
        """
        Initializes the DetectionsSmoothing object.

        Args:
            N (int): Number of samples to consider for smoothing.
        """
        self.N = N
        self.detections_history = []

    def calculate_mode_of_detections(self, detections_per_row):
        """
        Calculates the mode of detections per row over the last N samples.

        Args:
            detections_per_row (list): The current detections per row.

        Returns:
            list: Smoothed detections per row.
        """
        # Append new detections and keep only the last N samples
        self.detections_history.append(detections_per_row)
        self.detections_history = self.detections_history[-self.N:]
        
        # Determine the most common length of the lists in detections_history
        lengths = [len(lst) for lst in self.detections_history]
        try:
            common_length = mode(lengths)
        except StatisticsError:
            common_length = np.median(lengths)  # Fallback to median if no mode
        
        # Initialize the result list
        mode_detections = []

        # Calculate the mode for each position up to the common length
        for i in range(int(common_length)):
            elements_at_i = [lst[i] for lst in self.detections_history if len(lst) > i]
            try:
                mode_detections.append(mode(elements_at_i))
            except StatisticsError:
                mode_detections.append(int(np.median(elements_at_i)))  # Fallback to median if no mode

        return mode_detections
