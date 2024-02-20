def detect_rows(centroids, y_threshold=10):
    """
    Group centroids into rows based on their Y-coordinate proximity and count the detections in each row.
    
    Args:
        centroids (list): A list of [x, y] coordinates for each detected centroid.
        y_threshold (int): The Y-coordinate threshold to consider centroids as being in the same row.

    Returns:
        list: A list indicating the number of detections in each identified row.
    """
    # Sort centroids by y-coordinate to process them in vertical order
    centroids.sort(key=lambda x: x[1])

    # Initialize the first row and rows list
    rows = []
    current_row = [centroids[0]]

    for centroid in centroids[1:]:
        # If the current centroid is close enough to the previous one in the y-direction, add it to the current row
        if abs(centroid[1] - current_row[-1][1]) < y_threshold:
            current_row.append(centroid)
        else:
            # Otherwise, start a new row
            rows.append(current_row)
            current_row = [centroid]

    # Add the last row
    rows.append(current_row)

    # Count the number of detections in each row
    detections_per_row = [len(row) for row in rows]

    return detections_per_row
