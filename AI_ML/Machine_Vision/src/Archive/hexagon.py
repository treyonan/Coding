import cv2
import numpy as np

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

def detect_hexagons(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 30, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) < 50:
            continue
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.03 * peri, True)
        if is_hexagon(approx):
            cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
            # Calculate the centroid of the hexagon
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                # Draw the centroid on the frame
                cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
    return frame

# Start video capture
cap = cv2.VideoCapture(1)  # Use 0 for the default camera

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Process the frame for hexagon detection and centroid calculation
    processed_frame = detect_hexagons(frame)

    # Display the processed frame
    cv2.imshow('Hexagons Detected', processed_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
