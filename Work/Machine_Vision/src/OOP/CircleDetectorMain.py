import cv2
from lib.KMeansDetector import KMeansCircleDetector
from lib.DBSCANDetector import DBSCANCircleDetector
from lib.RandomCircleGenerator import update_image_periodically, stop_update_with_circles
from lib.CircleArrangementDetector import CircleArrangementDetector


def run_detection(detector, generate_circles=False):
    cap = cv2.VideoCapture(0)
    arrangement_detector = CircleArrangementDetector(eps=50, min_samples=1, sample_size=30)
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        detected_circles = detector.detect_circles_and_draw(frame)
        arrangement_detector.update_and_aggregate_counts(detected_circles)
        
        if frame_count % 30 == 0:
            common_counts = arrangement_detector.get_most_common_counts()
            print(f"Common circle counts per row: {common_counts}")
            #arrangement_detector.reset_counts_history()

        frame_count += 1
        cv2.imshow('Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
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

