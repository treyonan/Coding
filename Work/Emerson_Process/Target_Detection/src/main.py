import cv2
import customtkinter as ctk
import tkinter as tk
import threading

CAMERA_INDEX = 1
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Targets (relative to frame size)
# Centers defined as fractions so they move with the frame
TARGET1_REL_X = 0.33
TARGET1_REL_Y = 0.50
TARGET1_DIAMETER = 40  # pixels

TARGET2_REL_X = 0.66
TARGET2_REL_Y = 0.50
TARGET2_DIAMETER = 40  # pixels

# Shared state for GUI and camera thread
_stop_event = threading.Event()


def detect_largest_red_circle(frame):
    """Return (x, y, r) for the largest red circle found, else None.
    Uses HSV thresholding to isolate red, then HoughCircles on the mask.
    """
    # Slight blur to reduce noise before HSV thresholding
    blurred = cv2.GaussianBlur(frame, (9, 9), 2)

    # Convert to HSV and threshold for red (two ranges due to hue wrap-around)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    lower_red1 = (0, 100, 80)
    upper_red1 = (10, 255, 255)
    lower_red2 = (160, 100, 80)
    upper_red2 = (180, 255, 255)
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Clean up mask a bit for more stable circle detection
    mask = cv2.medianBlur(mask, 5)

    # HoughCircles expects an 8-bit single-channel image; the mask fits
    circles = cv2.HoughCircles(
        mask,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=30,
        param1=100,
        param2=15,
        minRadius=5,
        maxRadius=0,
    )

    if circles is not None and len(circles) > 0:
        circles = circles[0]
        # Select the largest circle by radius
        x, y, r = max(circles, key=lambda c: c[2])
        return int(x), int(y), int(r)

    return None


def run_camera(stop_event: threading.Event):
    cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print(f"Error: Cannot open camera index {CAMERA_INDEX}")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    window_name = "Target Detection"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    try:
        while not stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                print("Warning: Failed to read frame from camera")
                break

            circle = detect_largest_red_circle(frame)
            display = frame.copy()

            # Compute targets' centers in pixels (relative to current frame size)
            h, w = display.shape[:2]
            t1_x = int(TARGET1_REL_X * w)
            t1_y = int(TARGET1_REL_Y * h)
            t1_r = TARGET1_DIAMETER // 2
            t2_x = int(TARGET2_REL_X * w)
            t2_y = int(TARGET2_REL_Y * h)
            t2_r = TARGET2_DIAMETER // 2

            # Draw target circles (red outline)
            cv2.circle(display, (t1_x, t1_y), t1_r, (0, 0, 255), 2)
            cv2.circle(display, (t2_x, t2_y), t2_r, (0, 0, 255), 2)

            if circle is not None:
                x, y, r = circle
                cv2.circle(display, (x, y), r, (255, 0, 0), 2)
                cv2.circle(display, (x, y), 3, (255, 0, 0), -1)

                text = f"center: ({x}, {y})"
                cv2.putText(
                    display,
                    text,
                    (x + 10, max(20, y - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 0, 0),
                    2,
                    cv2.LINE_AA,
                )

            # Determine if the red circle center is inside each target
            hit1 = False
            hit2 = False
            if circle is not None:
                x, y, _ = circle
                dx1 = x - t1_x
                dy1 = y - t1_y
                hit1 = (dx1 * dx1 + dy1 * dy1) <= (t1_r * t1_r)
                dx2 = x - t2_x
                dy2 = y - t2_y
                hit2 = (dx2 * dx2 + dy2 * dy2) <= (t2_r * t2_r)

            # Draw target status texts in fixed HUD positions
            hud1_text = f"Target 1( cx={t1_x}, cy={t1_y} )"
            hud2_text = f"Target 2( cx={t2_x}, cy={t2_y} )"
            hud1_color = (0, 200, 0) if hit1 else (255, 255, 255)
            hud2_color = (0, 200, 0) if hit2 else (255, 255, 255)
            cv2.putText(display, hud1_text, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, hud1_color, 2, cv2.LINE_AA)
            cv2.putText(display, hud2_text, (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, hud2_color, 2, cv2.LINE_AA)

            cv2.imshow(window_name, display)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                stop_event.set()
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()


def start_gui(stop_event: threading.Event):
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Target Control")

    # Poll the stop flag so pressing 'q' in the camera window closes the GUI
    def _poll_stop():
        if stop_event.is_set():
            try:
                root.destroy()
            except Exception:
                pass
        else:
            root.after(50, _poll_stop)
    root.after(50, _poll_stop)

    # Frame for sliders
    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand=True, padx=12, pady=12)

    # Initial slider values in pixels for Target 1
    init1_x_px = int(TARGET1_REL_X * FRAME_WIDTH)
    init1_y_px = int(TARGET1_REL_Y * FRAME_HEIGHT)
    init1_d_px = int(TARGET1_DIAMETER)

    # Target 1 Controls
    lbl1_title = ctk.CTkLabel(frame, text="Target 1 Controls")
    lbl1_title.pack(anchor="w", pady=(0, 6))

    val1_x = tk.StringVar(value=f"X: {init1_x_px}")
    val1_y = tk.StringVar(value=f"Y: {init1_y_px}")
    val1_d = tk.StringVar(value=f"Diameter: {init1_d_px}")

    lbl1_x = ctk.CTkLabel(frame, textvariable=val1_x)
    lbl1_x.pack(anchor="w")
    sld1_x = ctk.CTkSlider(frame, from_=0, to=FRAME_WIDTH,
                           number_of_steps=FRAME_WIDTH)
    sld1_x.set(init1_x_px)
    sld1_x.pack(fill="x", pady=(0, 8))

    lbl1_y = ctk.CTkLabel(frame, textvariable=val1_y)
    lbl1_y.pack(anchor="w")
    sld1_y = ctk.CTkSlider(frame, from_=0, to=FRAME_HEIGHT,
                           number_of_steps=FRAME_HEIGHT)
    sld1_y.set(init1_y_px)
    sld1_y.pack(fill="x", pady=(0, 8))

    lbl1_d = ctk.CTkLabel(frame, textvariable=val1_d)
    lbl1_d.pack(anchor="w")
    sld1_d = ctk.CTkSlider(frame, from_=5, to=min(
        FRAME_WIDTH, FRAME_HEIGHT), number_of_steps=min(FRAME_WIDTH, FRAME_HEIGHT))
    sld1_d.set(init1_d_px)
    sld1_d.pack(fill="x", pady=(0, 8))

    def on_x1(val):
        global TARGET1_REL_X
        x_px = int(float(val))
        TARGET1_REL_X = max(0.0, min(1.0, x_px / FRAME_WIDTH))
        val1_x.set(f"X: {x_px}")

    def on_y1(val):
        global TARGET1_REL_Y
        y_px = int(float(val))
        TARGET1_REL_Y = max(0.0, min(1.0, y_px / FRAME_HEIGHT))
        val1_y.set(f"Y: {y_px}")

    def on_d1(val):
        global TARGET1_DIAMETER
        d_px = int(float(val))
        TARGET1_DIAMETER = max(5, d_px)
        val1_d.set(f"Diameter: {TARGET1_DIAMETER}")

    sld1_x.configure(command=on_x1)
    sld1_y.configure(command=on_y1)
    sld1_d.configure(command=on_d1)

    # Spacer
    ctk.CTkLabel(frame, text="").pack(pady=(8, 0))

    # Initial slider values in pixels for Target 2
    init2_x_px = int(TARGET2_REL_X * FRAME_WIDTH)
    init2_y_px = int(TARGET2_REL_Y * FRAME_HEIGHT)
    init2_d_px = int(TARGET2_DIAMETER)

    # Target 2 Controls
    lbl2_title = ctk.CTkLabel(frame, text="Target 2 Controls")
    lbl2_title.pack(anchor="w", pady=(0, 6))

    val2_x = tk.StringVar(value=f"X: {init2_x_px}")
    val2_y = tk.StringVar(value=f"Y: {init2_y_px}")
    val2_d = tk.StringVar(value=f"Diameter: {init2_d_px}")

    lbl2_x = ctk.CTkLabel(frame, textvariable=val2_x)
    lbl2_x.pack(anchor="w")
    sld2_x = ctk.CTkSlider(frame, from_=0, to=FRAME_WIDTH,
                           number_of_steps=FRAME_WIDTH)
    sld2_x.set(init2_x_px)
    sld2_x.pack(fill="x", pady=(0, 8))

    lbl2_y = ctk.CTkLabel(frame, textvariable=val2_y)
    lbl2_y.pack(anchor="w")
    sld2_y = ctk.CTkSlider(frame, from_=0, to=FRAME_HEIGHT,
                           number_of_steps=FRAME_HEIGHT)
    sld2_y.set(init2_y_px)
    sld2_y.pack(fill="x", pady=(0, 8))

    lbl2_d = ctk.CTkLabel(frame, textvariable=val2_d)
    lbl2_d.pack(anchor="w")
    sld2_d = ctk.CTkSlider(frame, from_=5, to=min(
        FRAME_WIDTH, FRAME_HEIGHT), number_of_steps=min(FRAME_WIDTH, FRAME_HEIGHT))
    sld2_d.set(init2_d_px)
    sld2_d.pack(fill="x", pady=(0, 8))

    def on_x2(val):
        global TARGET2_REL_X
        x_px = int(float(val))
        TARGET2_REL_X = max(0.0, min(1.0, x_px / FRAME_WIDTH))
        val2_x.set(f"X: {x_px}")

    def on_y2(val):
        global TARGET2_REL_Y
        y_px = int(float(val))
        TARGET2_REL_Y = max(0.0, min(1.0, y_px / FRAME_HEIGHT))
        val2_y.set(f"Y: {y_px}")

    def on_d2(val):
        global TARGET2_DIAMETER
        d_px = int(float(val))
        TARGET2_DIAMETER = max(5, d_px)
        val2_d.set(f"Diameter: {TARGET2_DIAMETER}")

    sld2_x.configure(command=on_x2)
    sld2_y.configure(command=on_y2)
    sld2_d.configure(command=on_d2)

    def on_close():
        stop_event.set()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


def main():
    # Start camera processing in a background thread
    cam_thread = threading.Thread(
        target=run_camera, args=(_stop_event,), daemon=True)
    cam_thread.start()

    # Start the GUI (blocks until closed)
    start_gui(_stop_event)

    # Ensure camera thread ends
    _stop_event.set()
    cam_thread.join(timeout=1.0)


if __name__ == "__main__":
    main()
