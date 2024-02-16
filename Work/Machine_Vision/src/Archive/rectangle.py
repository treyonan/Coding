import cv2
import numpy as np

def detect_rectangles(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 30, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) < 50:
            continue
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.03 * peri, True)
        if len(approx) == 4:
            cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)

            # Use minAreaRect to get the bounding box for the rotated rectangle
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            # Identify upper-left and lower-right corners
            sorted_box = box[np.argsort(box[:, 0])]
            left_most = sorted_box[:2]
            right_most = sorted_box[2:]

            upper_left = left_most[np.argmin(left_most[:, 1])]
            lower_right = right_most[np.argmax(right_most[:, 1])]

            # Draw red dots on the upper-left and lower-right corners
            cv2.circle(frame, tuple(upper_left), 5, (0, 0, 255), -1)
            cv2.circle(frame, tuple(lower_right), 5, (0, 0, 255), -1)

            # Print X and Y value pairs for the corner points
            print(f"Upper Left: {tuple(upper_left)}, Lower Right: {tuple(lower_right)}")

    return frame

# Start video capture
cap = cv2.VideoCapture(1)  # Adjust the camera index if necessary

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Process the frame for rectangle detection
    processed_frame = detect_rectangles(frame)

    # Display the processed frame
    cv2.imshow('Rectangles Detected', processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


