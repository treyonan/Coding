import cv2
import customtkinter as ctk
import tkinter as tk
import threading
import json
import os
import math

CAMERA_INDEX = 1
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Rendering / smoothing
DEADBAND_PX = 6  # Only update drawn center if movement exceeds this many pixels

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


def _settings_path():
    # Save settings one directory up from src/, at project root
    base_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), os.pardir))
    return os.path.join(base_dir, "settings.json")


def load_settings():
    global CAMERA_INDEX, TARGET1_REL_X, TARGET1_REL_Y, TARGET1_DIAMETER
    global TARGET2_REL_X, TARGET2_REL_Y, TARGET2_DIAMETER
    global DEADBAND_PX

    path = _settings_path()
    if not os.path.exists(path):
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Warning: Failed to load settings: {e}")
        return

    try:
        CAMERA_INDEX = int(data.get("camera_index", CAMERA_INDEX))
        fw = int(data.get("frame_width", FRAME_WIDTH)) or FRAME_WIDTH
        fh = int(data.get("frame_height", FRAME_HEIGHT)) or FRAME_HEIGHT

        t1 = data.get("target1", {})
        t1x = int(t1.get("x", int(TARGET1_REL_X * fw)))
        t1y = int(t1.get("y", int(TARGET1_REL_Y * fh)))
        TARGET1_DIAMETER = int(t1.get("diameter", TARGET1_DIAMETER))
        # Convert to relative for internal state
        TARGET1_REL_X = max(0.0, min(1.0, t1x / fw))
        TARGET1_REL_Y = max(0.0, min(1.0, t1y / fh))

        t2 = data.get("target2", {})
        t2x = int(t2.get("x", int(TARGET2_REL_X * fw)))
        t2y = int(t2.get("y", int(TARGET2_REL_Y * fh)))
        TARGET2_DIAMETER = int(t2.get("diameter", TARGET2_DIAMETER))
        TARGET2_REL_X = max(0.0, min(1.0, t2x / fw))
        TARGET2_REL_Y = max(0.0, min(1.0, t2y / fh))

        # Optional rendering settings
        DEADBAND_PX = int(data.get("deadband_px", DEADBAND_PX))
    except Exception as e:
        print(f"Warning: Invalid settings content, using defaults: {e}")


def save_settings():
    # Persist pixel-based positions for the configured frame size
    t1x = int(TARGET1_REL_X * FRAME_WIDTH)
    t1y = int(TARGET1_REL_Y * FRAME_HEIGHT)
    t2x = int(TARGET2_REL_X * FRAME_WIDTH)
    t2y = int(TARGET2_REL_Y * FRAME_HEIGHT)

    data = {
        "camera_index": CAMERA_INDEX,
        "frame_width": FRAME_WIDTH,
        "frame_height": FRAME_HEIGHT,
        "target1": {"x": t1x, "y": t1y, "diameter": int(TARGET1_DIAMETER)},
        "target2": {"x": t2x, "y": t2y, "diameter": int(TARGET2_DIAMETER)},
        "deadband_px": int(DEADBAND_PX),
    }

    path = _settings_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Warning: Failed to save settings: {e}")


def detect_red_circles(frame, max_count: int = 2):
    """Return up to `max_count` red circles as a list of (x, y, r).
    HSV thresholding for red + morphology + HoughCircles.
    """
    blurred = cv2.GaussianBlur(frame, (9, 9), 2)

    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    lower_red1 = (0, 100, 80)
    upper_red1 = (10, 255, 255)
    lower_red2 = (160, 100, 80)
    upper_red2 = (180, 255, 255)
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Stabilize detections
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.medianBlur(mask, 5)

    circles = cv2.HoughCircles(
        mask,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=24,
        param1=100,
        param2=16,
        minRadius=4,
        maxRadius=0,
    )

    candidates = []
    if circles is not None and len(circles) > 0:
        h, w = mask.shape[:2]
        for (x_f, y_f, r_f) in circles[0]:
            x = int(x_f)
            y = int(y_f)
            r = int(r_f)
            # Skip degenerate
            if r <= 0:
                continue

            # ROI around the circle
            x0 = max(0, x - r)
            y0 = max(0, y - r)
            x1 = min(w, x + r)
            y1 = min(h, y + r)
            if x1 <= x0 or y1 <= y0:
                continue

            sub = mask[y0:y1, x0:x1]

            # Find the largest contour in this ROI
            cnts, _ = cv2.findContours(
                sub, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not cnts:
                continue
            cnt = max(cnts, key=cv2.contourArea)
            area = float(cv2.contourArea(cnt))
            perim = float(cv2.arcLength(cnt, True))
            if perim <= 0.0 or area <= 0.0:
                continue

            circularity = 4.0 * math.pi * area / (perim * perim)

            # Compute fill ratio: area of red within the ideal circle area
            # Create a circular mask within ROI
            circle_mask = sub.copy()
            circle_mask[:] = 0
            cv2.circle(circle_mask, (x - x0, y - y0),
                       r, color=255, thickness=-1)
            filled = cv2.bitwise_and(sub, circle_mask)
            red_area_inside_circle = float(cv2.countNonZero(filled))
            circle_area = math.pi * (r ** 2)
            fill_ratio = red_area_inside_circle / circle_area if circle_area > 0 else 0.0

            # Thresholds: tune if needed
            if circularity >= 0.87 and 0.75 <= fill_ratio <= 1.25:
                candidates.append((x, y, r))

    # If we still have fewer than desired circles, upsample mask and try again
    if len(candidates) < max_count:
        mask_up = cv2.resize(mask, None, fx=2.0, fy=2.0,
                             interpolation=cv2.INTER_LINEAR)
        circles2 = cv2.HoughCircles(
            mask_up,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=48,     # scaled with 2x
            param1=100,
            param2=16,
            minRadius=8,    # scaled with 2x
            maxRadius=0,
        )
        if circles2 is not None and len(circles2) > 0:
            h, w = mask.shape[:2]
            for (x2, y2, r2) in circles2[0]:
                x = int(round(x2 / 2.0))
                y = int(round(y2 / 2.0))
                r = int(round(r2 / 2.0))
                if r <= 0:
                    continue
                # Validate at original scale using the same criteria
                x0 = max(0, x - r)
                y0 = max(0, y - r)
                x1 = min(w, x + r)
                y1 = min(h, y + r)
                if x1 <= x0 or y1 <= y0:
                    continue
                sub = mask[y0:y1, x0:x1]
                cnts, _ = cv2.findContours(
                    sub, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if not cnts:
                    continue
                cnt = max(cnts, key=cv2.contourArea)
                area = float(cv2.contourArea(cnt))
                perim = float(cv2.arcLength(cnt, True))
                if perim <= 0.0 or area <= 0.0:
                    continue
                circularity = 4.0 * math.pi * area / (perim * perim)
                circle_mask = sub.copy()
                circle_mask[:] = 0
                cv2.circle(circle_mask, (x - x0, y - y0),
                           r, color=255, thickness=-1)
                filled = cv2.bitwise_and(sub, circle_mask)
                red_area_inside_circle = float(cv2.countNonZero(filled))
                circle_area = math.pi * (r ** 2)
                fill_ratio = red_area_inside_circle / circle_area if circle_area > 0 else 0.0
                if circularity >= 0.87 and 0.75 <= fill_ratio <= 1.25:
                    # Deduplicate by center proximity (<=5 px)
                    dup = False
                    for (ex, ey, er) in candidates:
                        if (ex - x) * (ex - x) + (ey - y) * (ey - y) <= 25:
                            dup = True
                            break
                    if not dup:
                        candidates.append((x, y, r))

    # Sort by radius and keep up to max_count
    candidates.sort(key=lambda c: c[2], reverse=True)
    candidates = candidates[:max_count]

    return candidates


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
        prev_displayed = []  # Previously drawn circle centers [(x,y,r), ...]
        last_hit1 = False
        last_hit2 = False
        while not stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                print("Warning: Failed to read frame from camera")
                break

            circles = detect_red_circles(frame, max_count=2)
            display = frame.copy()

            # Compute targets' centers in pixels (relative to current frame size)
            h, w = display.shape[:2]
            t1_x = int(TARGET1_REL_X * w)
            t1_y = int(TARGET1_REL_Y * h)
            t1_r = TARGET1_DIAMETER // 2
            t2_x = int(TARGET2_REL_X * w)
            t2_y = int(TARGET2_REL_Y * h)
            t2_r = TARGET2_DIAMETER // 2

            # Draw target circles (blue outline) with dynamic thickness
            t1_th = max(1, int(t1_r // 12))
            t2_th = max(1, int(t2_r // 12))
            cv2.circle(display, (t1_x, t1_y), t1_r, (255, 0, 0), t1_th)
            cv2.circle(display, (t2_x, t2_y), t2_r, (255, 0, 0), t2_th)

            # Build smoothed/displayed circles using deadband on center position only
            next_displayed = []
            for i, (x, y, r) in enumerate(circles):
                if i < len(prev_displayed):
                    px, py, pr = prev_displayed[i]
                    if px is not None and py is not None:
                        dx = x - px
                        dy = y - py
                        if (dx * dx + dy * dy) <= (DEADBAND_PX * DEADBAND_PX):
                            # Keep previous center to reduce flicker; update radius from realtime
                            next_displayed.append((px, py, r))
                            continue
                next_displayed.append((x, y, r))

            # Draw smoothed circles (in green) and annotate centers with dynamic thickness
            for idx, (dx_, dy_, r_) in enumerate(next_displayed):
                c_th = max(1, int(r_ // 12))
                cv2.circle(display, (dx_, dy_), r_, (0, 255, 0), c_th)
                cv2.circle(display, (dx_, dy_), 3, (0, 255, 0), -1)
                text = f"center {idx+1}: ({dx_}, {dy_})"
                cv2.putText(
                    display,
                    text,
                    (dx_ + 10, max(20, dy_ - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )
            prev_displayed = next_displayed

            # Determine if the red circle center is inside each target
            # Debounced hit logic using hysteresis based on DEADBAND_PX
            # Compute best (max) inside margin for each target across all circles
            best_margin1 = float('-inf')
            best_margin2 = float('-inf')
            for (x, y, _) in circles:  # real-time positions
                # margin = target_radius - distance_to_center (positive -> inside)
                d1 = math.hypot(x - t1_x, y - t1_y)
                d2 = math.hypot(x - t2_x, y - t2_y)
                best_margin1 = max(best_margin1, t1_r - d1)
                best_margin2 = max(best_margin2, t2_r - d2)

            # Apply hysteresis: turn ON only when clearly inside by deadband; OFF when clearly outside
            hit1 = last_hit1
            if not last_hit1:
                if best_margin1 >= DEADBAND_PX:
                    hit1 = True
            else:
                if best_margin1 <= -DEADBAND_PX:
                    hit1 = False

            hit2 = last_hit2
            if not last_hit2:
                if best_margin2 >= DEADBAND_PX:
                    hit2 = True
            else:
                if best_margin2 <= -DEADBAND_PX:
                    hit2 = False

            last_hit1, last_hit2 = hit1, hit2

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
                # Save once when quitting via keyboard
                try:
                    save_settings()
                except Exception:
                    pass
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
                # Save before closing if needed
                try:
                    save_settings()
                except Exception:
                    pass
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

    # Spacer
    ctk.CTkLabel(frame, text="").pack(pady=(8, 0))

    # Rendering settings
    lblr_title = ctk.CTkLabel(frame, text="Rendering")
    lblr_title.pack(anchor="w", pady=(0, 6))

    val_dead = tk.StringVar(value=f"Deadband: {DEADBAND_PX} px")
    lbl_dead = ctk.CTkLabel(frame, textvariable=val_dead)
    lbl_dead.pack(anchor="w")
    sld_dead = ctk.CTkSlider(frame, from_=0, to=30, number_of_steps=30)
    sld_dead.set(DEADBAND_PX)
    sld_dead.pack(fill="x", pady=(0, 8))

    def on_dead(val):
        global DEADBAND_PX
        DEADBAND_PX = int(float(val))
        val_dead.set(f"Deadband: {DEADBAND_PX} px")

    sld_dead.configure(command=on_dead)

    def on_close():
        stop_event.set()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


def main():
    # Load persisted settings (if available)
    load_settings()

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
