import cv2
import numpy as np

class CentroidTracker:
    def __init__(self, maxFrames=10):
        self.maxFrames = maxFrames
        self.history = []

    def update(self, centroids):
        self.history.append(centroids)
        if len(self.history) > self.maxFrames:
            self.history.pop(0)

    def is_consistent(self, centroid):
        if not self.history:
            return True
        for prev_centroids in reversed(self.history):
            if any(np.linalg.norm(np.array(centroid) - np.array(pc)) < 20 for pc in prev_centroids):
                return True
        return False

def angle_cos(p0, p1, p2):
    d1, d2 = (p0 - p1).astype('float'), (p0 - p2).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2)))

def is_hexagon(approx):
    if len(approx) != 6:
        return False
    x, y, w, h = cv2.boundingRect(approx)
    aspect_ratio = float(w) / h
    if not 0.7 < aspect_ratio < 1.3:
        return False
    angle_checks = []
    for i in range(6):
        angle = angle_cos(approx[i][0], approx[(i+1) % 6][0], approx[(i+2) % 6][0])
        if 0.3 < angle < 0.9:
            angle_checks.append(True)
        else:
            angle_checks.append(False)
    return sum(angle_checks) >= 4

def detect_hexagons(frame, tracker):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 30, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    current_frame_centroids = []
    for contour in contours:
        if cv2.contourArea(contour) < 50:
            continue
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.05 * peri, True)
        if is_hexagon(approx):
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                current_frame_centroids.append((cX, cY))
                if tracker.is_consistent((cX, cY)):
                    cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
                    cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
    
    tracker.update(current_frame_centroids)
    return frame

# Initialize the centroid tracker
tracker = CentroidTracker(maxFrames=5)

# Start video capture
cap = cv2.VideoCapture(1)  # Use 0 for the default camera

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Process the frame for hexagon detection
    processed_frame = detect_hexagons(frame, tracker)

    # Display the processed frame
    cv2.imshow('Hexagons Detected', processed_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
