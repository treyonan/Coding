import cv2
from lib.KMeansDetector import KMeansCircleDetector
from lib.DBSCANDetector import DBSCANCircleDetector
from lib.RandomCircleGenerator import update_image_periodically, stop_update_with_circles

def run_detection(detector, generate_circles=False):
    cap = cv2.VideoCapture(1)
    stop_event = None
    if generate_circles:
        window_name = "Random Circles"
        stop_event = update_image_periodically(window_name, interval=5)  # Update every 5 seconds

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        detector.detect_circles_and_draw(frame)
        cv2.imshow('Detection', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    # Signal the thread to stop and ensure all windows are closed
    if generate_circles:
        stop_update_with_circles(stop_event)
    
    cap.release()
    # Ensure all OpenCV windows are closed
    cv2.destroyAllWindows()


def main():
    print("Choose the detection method:")
    print("1: KMeans")
    print("2: DBSCAN")
    choice = input("Enter choice: ")
    generate_circles = input("Generate random circles? (y/n): ").lower() == 'y'

    if choice == '1':
        detector = KMeansCircleDetector(num_clusters=3)
    elif choice == '2':
        detector = DBSCANCircleDetector(eps=10, min_samples=5)
    else:
        print("Invalid choice.")
        return

    run_detection(detector, generate_circles)

if __name__ == "__main__":
    main()

