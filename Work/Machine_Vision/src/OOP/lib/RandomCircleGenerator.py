import cv2
import numpy as np
import random
import threading
import time

def draw_random_circles(img, num_circles=10, radius_range=(20, 50)):
    max_attempts = 1000
    circles = []

    for _ in range(num_circles):
        for _ in range(max_attempts):
            radius = random.randint(*radius_range)
            x = random.randint(radius, img.shape[1] - radius)
            y = random.randint(radius, img.shape[0] - radius)

            overlap = False
            for cx, cy, cr in circles:
                distance = np.sqrt((cx - x)**2 + (cy - y)**2)
                if distance < (cr + radius):
                    overlap = True
                    break

            if not overlap:
                circles.append((x, y, radius))
                cv2.circle(img, (x, y), radius, (255, 0, 0), 2)
                break

    # After drawing all circles, add text indicating the number of circles
    text = f'Circles: {len(circles)}'
    cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

def update_image_periodically(window_name, img_shape=(480, 640, 3), circle_range=(5, 20), interval=5):
    def update_task():
        while not stop_event.is_set():
            num_circles = random.randint(*circle_range)  # Choose a random number of circles
            img = np.zeros(img_shape, dtype=np.uint8)
            draw_random_circles(img, num_circles=num_circles)
            cv2.imshow(window_name, img)
            cv2.waitKey(1)  # Use a short delay to ensure the window responds
            time.sleep(interval)  # Wait for the specified interval between updates

    stop_event = threading.Event()
    thread = threading.Thread(target=update_task)
    thread.start()
    return stop_event  # Return the stop event to control the thread outside

def stop_update_with_circles(stop_event):
    stop_event.set()  # Signal the thread to stop
