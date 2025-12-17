# REV 1.0 - Added faster contour mode and toggle from gui - 11/12/2025 - T. O'Nan

import cv2
import customtkinter as ctk
import tkinter as tk
import threading
import json
import os
import math
import time
import platform

try:
    # PLC helpers (optional). If pylogix is missing, we just skip PLC writes.
    from utils.pylogix import init_default as plc_init_default, update_default as plc_update_default, shutdown_default as plc_shutdown_default
    _PLC_AVAILABLE = True
    _PLC_IMPORT_ERROR = None
except Exception as _e:
    _PLC_AVAILABLE = False
    _PLC_IMPORT_ERROR = _e

CAMERA_INDEX = 1
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CURRENT_FRAME_WIDTH = FRAME_WIDTH
CURRENT_FRAME_HEIGHT = FRAME_HEIGHT
CURRENT_FPS = 0.0

# Rendering / smoothing
DEFAULT_DEADBAND_PX = 1
# Only update drawn center if movement exceeds this many pixels
DEADBAND_PX = DEFAULT_DEADBAND_PX

# Detection parameters (tunable)
DEFAULT_HOUGH_PARAM2 = 8  # Lower = more detections (more false positives)
DEFAULT_MIN_RADIUS = 4     # Minimum circle radius in pixels
HOUGH_PARAM2 = DEFAULT_HOUGH_PARAM2
MIN_RADIUS = DEFAULT_MIN_RADIUS

# Temporal stability (consecutive-frames filters)
DEFAULT_ON_FRAMES = 3
DEFAULT_OFF_FRAMES = 3
DEFAULT_APPEAR_FRAMES = 2
DEFAULT_HOLD_FRAMES = 4
ON_FRAMES = DEFAULT_ON_FRAMES
OFF_FRAMES = DEFAULT_OFF_FRAMES
APPEAR_FRAMES = DEFAULT_APPEAR_FRAMES
HOLD_FRAMES = DEFAULT_HOLD_FRAMES

# Unified stability control
DEFAULT_STABILITY_FRAMES = 3
STABILITY_FRAMES = DEFAULT_STABILITY_FRAMES

# Detection mode toggle (True = fast, False = Hughes)
USE_FAST_DETECTION = False

# Debug view
SHOW_MASK = False

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
    global CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT
    global TARGET1_REL_X, TARGET1_REL_Y, TARGET1_DIAMETER
    global TARGET2_REL_X, TARGET2_REL_Y, TARGET2_DIAMETER
    global DEADBAND_PX, HOUGH_PARAM2, MIN_RADIUS, SHOW_MASK
    global ON_FRAMES, OFF_FRAMES, APPEAR_FRAMES, HOLD_FRAMES
    global STABILITY_FRAMES
    global USE_FAST_DETECTION

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
        # Apply loaded frame size to globals so it persists across runs
        FRAME_WIDTH = fw
        FRAME_HEIGHT = fh

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

        # Optional rendering / detection settings
        DEADBAND_PX = int(data.get("deadband_px", DEADBAND_PX))
        HOUGH_PARAM2 = int(data.get("hough_param2", HOUGH_PARAM2))
        MIN_RADIUS = int(data.get("min_radius", MIN_RADIUS))
        SHOW_MASK = bool(data.get("show_mask", SHOW_MASK))
        # Prefer unified stability control if present
        STABILITY_FRAMES = int(data.get("stability_frames", STABILITY_FRAMES))
        # Legacy keys fallback
        ON_FRAMES = int(data.get("on_frames", ON_FRAMES))
        OFF_FRAMES = int(data.get("off_frames", OFF_FRAMES))
        APPEAR_FRAMES = int(data.get("appear_frames", APPEAR_FRAMES))
        HOLD_FRAMES = int(data.get("hold_frames", HOLD_FRAMES))
        # Derive from unified stability (overrides legacy)
        if STABILITY_FRAMES is not None:
            ON_FRAMES = 1
            OFF_FRAMES = max(1, STABILITY_FRAMES)
            APPEAR_FRAMES = 1
            HOLD_FRAMES = max(1, STABILITY_FRAMES * 2)
        USE_FAST_DETECTION = bool(
            data.get("fast_detection_mode", USE_FAST_DETECTION))
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
        "hough_param2": int(HOUGH_PARAM2),
        "min_radius": int(MIN_RADIUS),
        "show_mask": bool(SHOW_MASK),
        "on_frames": int(ON_FRAMES),
        "off_frames": int(OFF_FRAMES),
        "appear_frames": int(APPEAR_FRAMES),
        "hold_frames": int(HOLD_FRAMES),
        "stability_frames": int(STABILITY_FRAMES),
        "fast_detection_mode": bool(USE_FAST_DETECTION),
    }

    path = _settings_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Warning: Failed to save settings: {e}")


def create_red_mask(frame):
    """Create a binary mask for red regions with blur + HSV threshold + morphology."""
    blurred = cv2.GaussianBlur(frame, (9, 9), 2)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    lower_red1 = (0, 100, 80)
    upper_red1 = (10, 255, 255)
    lower_red2 = (160, 100, 80)
    upper_red2 = (180, 255, 255)
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.medianBlur(mask, 5)
    return mask

# = Hughes Circles =======================================================================


def detect_red_circles_houghes(frame, max_count: int = 2, mask=None):
    """Return up to `max_count` red circles as a list of (x, y, r)."""
    if mask is None:
        mask = create_red_mask(frame)

    min_dist = max(12, 6 * max(1, MIN_RADIUS))
    circles = cv2.HoughCircles(
        mask,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=int(min_dist),
        param1=100,
        param2=int(HOUGH_PARAM2),
        minRadius=int(MIN_RADIUS),
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
            minDist=int(min_dist * 2),     # scaled with 2x
            param1=100,
            param2=int(HOUGH_PARAM2),
            minRadius=int(max(2, MIN_RADIUS) * 2),    # scaled with 2x
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

# = FAST RED CIRCLES ==================================================================


def detect_red_circles(frame, max_count=2, mask=None):
    """Contour-based red detection (fast)."""
    if mask is None:
        mask = create_red_mask(frame)
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    results = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < 80:
            continue
        (x, y), r = cv2.minEnclosingCircle(c)
        r = int(r)
        if r < MIN_RADIUS or r > 100:
            continue
        perim = cv2.arcLength(c, True)
        if perim == 0:
            continue
        circularity = 4 * math.pi * area / (perim * perim)
        if circularity > 0.75:
            results.append((int(x), int(y), r))
    results.sort(key=lambda c: c[2], reverse=True)
    return results[:max_count]

# ======================================================================================


def run_camera(stop_event: threading.Event):
    if platform.system() == "Windows":
        cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_V4L2)

    if not cap.isOpened():
        print(f"Error: Cannot open camera index {CAMERA_INDEX}")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    # Record actual frame size
    try:
        w_actual = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h_actual = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if w_actual > 0 and h_actual > 0:
            global CURRENT_FRAME_WIDTH, CURRENT_FRAME_HEIGHT
            CURRENT_FRAME_WIDTH = w_actual
            CURRENT_FRAME_HEIGHT = h_actual
    except Exception:
        pass

    window_name = "Target Detection"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    try:
        prev_displayed = []  # Previously drawn circle centers [(x,y,r), ...]
        last_hit1 = False  # hysteresis state
        last_hit2 = False
        disp_hit1 = False  # displayed/PLC state after temporal filtering
        disp_hit2 = False
        off_count1 = 0
        off_count2 = 0
        hold_counts = [0, 0]
        mask_window_open = False
        # last applied size to the capture
        last_w_applied = CURRENT_FRAME_WIDTH
        last_h_applied = CURRENT_FRAME_HEIGHT
        # fps tracking
        last_ts = time.time()
        while not stop_event.is_set():
            # initialize per-loop states if missing
            # Apply resolution change on-the-fly if desired differs from actual
            try:
                if FRAME_WIDTH != last_w_applied or FRAME_HEIGHT != last_h_applied:
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
                    # Read back
                    w_actual = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    h_actual = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    if w_actual > 0 and h_actual > 0:
                        CURRENT_FRAME_WIDTH = w_actual
                        CURRENT_FRAME_HEIGHT = h_actual
                        last_w_applied = w_actual
                        last_h_applied = h_actual
            except Exception:
                pass
            ret, frame = cap.read()
            if not ret:
                print("Warning: Failed to read frame from camera")
                break

            # FPS update (exponential moving average for stability)
            try:
                now = time.time()
                dt = now - last_ts
                last_ts = now
                if dt > 0:
                    inst = 1.0 / dt
                    global CURRENT_FPS
                    if CURRENT_FPS > 0:
                        CURRENT_FPS = 0.85 * CURRENT_FPS + 0.15 * inst
                    else:
                        CURRENT_FPS = inst
            except Exception:
                pass

            mask = create_red_mask(frame)

            # Select detection mode based on USE_FAST_DETECTION flag
            if USE_FAST_DETECTION:
                circles = detect_red_circles(frame, max_count=2, mask=mask)
            else:
                circles = detect_red_circles_houghes(
                    frame, max_count=2, mask=mask)

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

            # Nearest-neighbor matching to keep IDs stable across frames
            # Order current circles to align with prev_displayed by proximity
            ordered_current = []
            remaining_curr = circles.copy()
            used_idx = set()
            if prev_displayed and remaining_curr:
                # Build pairwise distances
                pairs = []  # (dist2, prev_idx, curr_idx)
                for pi, (px, py, pr) in enumerate(prev_displayed):
                    for ci, (cx, cy, cr) in enumerate(remaining_curr):
                        d2 = (cx - px) * (cx - px) + (cy - py) * (cy - py)
                        pairs.append((d2, pi, ci))
                pairs.sort(key=lambda t: t[0])
                assigned_prev = set()
                assigned_curr = set()
                mapping = {}
                for d2, pi, ci in pairs:
                    if pi in assigned_prev or ci in assigned_curr:
                        continue
                    assigned_prev.add(pi)
                    assigned_curr.add(ci)
                    mapping[pi] = ci
                # Build ordered list by prev indices
                for pi in range(len(prev_displayed)):
                    ci = mapping.get(pi)
                    if ci is not None:
                        ordered_current.append(remaining_curr[ci])
                        used_idx.add(ci)
                    else:
                        ordered_current.append(None)
                # Append any new unmatched detections at the end
                for ci, c in enumerate(remaining_curr):
                    if ci not in used_idx:
                        ordered_current.append(c)
            else:
                ordered_current = remaining_curr

            # Build smoothed/displayed circles with hold and deadband on center
            next_displayed = []
            for i in range(0, max(2, len(ordered_current))):
                cur = ordered_current[i] if i < len(ordered_current) else None
                prev = prev_displayed[i] if i < len(prev_displayed) else None

                if cur is not None:
                    x, y, r = cur
                    if i < 2:
                        # Reset hold counter on any positive presence; draw immediately
                        hold_counts[i] = HOLD_FRAMES
                    if prev is not None:
                        px, py, pr = prev
                        dx = x - px
                        dy = y - py
                        if (dx * dx + dy * dy) <= (DEADBAND_PX * DEADBAND_PX):
                            next_displayed.append((px, py, r))
                            continue
                    next_displayed.append((x, y, r))
                else:
                    if i < 2 and prev is not None and hold_counts[i] > 0:
                        hold_counts[i] -= 1
                        next_displayed.append(prev)
                    else:
                        # nothing to draw for this slot
                        pass

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
            hit1_raw = last_hit1
            if not last_hit1:
                if best_margin1 >= DEADBAND_PX:
                    hit1_raw = True
            else:
                if best_margin1 <= -DEADBAND_PX:
                    hit1_raw = False

            hit2_raw = last_hit2
            if not last_hit2:
                if best_margin2 >= DEADBAND_PX:
                    hit2_raw = True
            else:
                if best_margin2 <= -DEADBAND_PX:
                    hit2_raw = False

            last_hit1, last_hit2 = hit1_raw, hit2_raw

            # Temporal filter: immediate ON; OFF only after OFF_FRAMES consecutive falses
            if hit1_raw:
                disp_hit1 = True
                off_count1 = 0
            else:
                off_count1 += 1
                if off_count1 >= OFF_FRAMES:
                    disp_hit1 = False
                    off_count1 = 0

            if hit2_raw:
                disp_hit2 = True
                off_count2 = 0
            else:
                off_count2 += 1
                if off_count2 >= OFF_FRAMES:
                    disp_hit2 = False
                    off_count2 = 0

            # Send debounced states to PLC (non-blocking writer thread)
            if _PLC_AVAILABLE:
                try:
                    plc_update_default(disp_hit1, disp_hit2)
                except Exception:
                    pass

            # Draw target status texts in fixed HUD positions
            hud1_text = f"Target 1( cx={t1_x}, cy={t1_y} )"
            hud2_text = f"Target 2( cx={t2_x}, cy={t2_y} )"
            hud1_color = (0, 200, 0) if disp_hit1 else (255, 255, 255)
            hud2_color = (0, 200, 0) if disp_hit2 else (255, 255, 255)
            cv2.putText(display, hud1_text, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, hud1_color, 2, cv2.LINE_AA)
            cv2.putText(display, hud2_text, (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, hud2_color, 2, cv2.LINE_AA)

            # Show which detection mode is active
            mode_text = "Mode: FAST (Contours)" if USE_FAST_DETECTION else "Mode: HUGHES (Hough Circles)"
            cv2.putText(display, mode_text, (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2, cv2.LINE_AA)

            cv2.imshow(window_name, display)
            # Optional mask window
            if SHOW_MASK:
                cv2.imshow("Red Mask", mask)
                mask_window_open = True
            else:
                if mask_window_open:
                    try:
                        cv2.destroyWindow("Red Mask")
                    except Exception:
                        pass
                    mask_window_open = False

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

    # Two-column layout to reduce height
    container = ctk.CTkFrame(root)
    container.pack(fill="both", expand=True, padx=12, pady=12)
    frame_left = ctk.CTkFrame(container)
    frame_left.pack(side="left", fill="both", expand=True, padx=(0, 6))
    frame_right = ctk.CTkFrame(container)
    frame_right.pack(side="left", fill="both", expand=True, padx=(6, 0))

    # Initial slider values in pixels for Target 1
    init1_x_px = int(TARGET1_REL_X * CURRENT_FRAME_WIDTH)
    init1_y_px = int(TARGET1_REL_Y * CURRENT_FRAME_HEIGHT)
    init1_d_px = int(TARGET1_DIAMETER)

    # Target 1 Controls
    lbl1_title = ctk.CTkLabel(frame_left, text="Target 1 Controls")
    lbl1_title.pack(anchor="w", pady=(0, 6))

    val1_x = tk.StringVar(value=f"X: {init1_x_px}")
    val1_y = tk.StringVar(value=f"Y: {init1_y_px}")
    val1_d = tk.StringVar(value=f"Diameter: {init1_d_px}")

    lbl1_x = ctk.CTkLabel(frame_left, textvariable=val1_x)
    lbl1_x.pack(anchor="w")
    sld1_x = ctk.CTkSlider(frame_left, from_=0, to=CURRENT_FRAME_WIDTH,
                           number_of_steps=CURRENT_FRAME_WIDTH)
    sld1_x.set(init1_x_px)
    sld1_x.pack(fill="x", pady=(0, 8))

    lbl1_y = ctk.CTkLabel(frame_left, textvariable=val1_y)
    lbl1_y.pack(anchor="w")
    sld1_y = ctk.CTkSlider(frame_left, from_=0, to=CURRENT_FRAME_HEIGHT,
                           number_of_steps=CURRENT_FRAME_HEIGHT)
    sld1_y.set(init1_y_px)
    sld1_y.pack(fill="x", pady=(0, 8))

    lbl1_d = ctk.CTkLabel(frame_left, textvariable=val1_d)
    lbl1_d.pack(anchor="w")
    sld1_d = ctk.CTkSlider(frame_left, from_=5, to=min(
        CURRENT_FRAME_WIDTH, CURRENT_FRAME_HEIGHT), number_of_steps=min(CURRENT_FRAME_WIDTH, CURRENT_FRAME_HEIGHT))
    sld1_d.set(init1_d_px)
    sld1_d.pack(fill="x", pady=(0, 8))

    def on_x1(val):
        global TARGET1_REL_X
        x_px = int(float(val))
        TARGET1_REL_X = max(0.0, min(1.0, x_px / max(1, CURRENT_FRAME_WIDTH)))
        val1_x.set(f"X: {x_px}")

    def on_y1(val):
        global TARGET1_REL_Y
        y_px = int(float(val))
        TARGET1_REL_Y = max(0.0, min(1.0, y_px / max(1, CURRENT_FRAME_HEIGHT)))
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
    ctk.CTkLabel(frame_left, text="").pack(pady=(8, 0))

    # Initial slider values in pixels for Target 2
    init2_x_px = int(TARGET2_REL_X * CURRENT_FRAME_WIDTH)
    init2_y_px = int(TARGET2_REL_Y * CURRENT_FRAME_HEIGHT)
    init2_d_px = int(TARGET2_DIAMETER)

    # Target 2 Controls
    lbl2_title = ctk.CTkLabel(frame_left, text="Target 2 Controls")
    lbl2_title.pack(anchor="w", pady=(0, 6))

    val2_x = tk.StringVar(value=f"X: {init2_x_px}")
    val2_y = tk.StringVar(value=f"Y: {init2_y_px}")
    val2_d = tk.StringVar(value=f"Diameter: {init2_d_px}")

    lbl2_x = ctk.CTkLabel(frame_left, textvariable=val2_x)
    lbl2_x.pack(anchor="w")
    sld2_x = ctk.CTkSlider(frame_left, from_=0, to=CURRENT_FRAME_WIDTH,
                           number_of_steps=CURRENT_FRAME_WIDTH)
    sld2_x.set(init2_x_px)
    sld2_x.pack(fill="x", pady=(0, 8))

    lbl2_y = ctk.CTkLabel(frame_left, textvariable=val2_y)
    lbl2_y.pack(anchor="w")
    sld2_y = ctk.CTkSlider(frame_left, from_=0, to=CURRENT_FRAME_HEIGHT,
                           number_of_steps=CURRENT_FRAME_HEIGHT)
    sld2_y.set(init2_y_px)
    sld2_y.pack(fill="x", pady=(0, 8))

    lbl2_d = ctk.CTkLabel(frame_left, textvariable=val2_d)
    lbl2_d.pack(anchor="w")
    sld2_d = ctk.CTkSlider(frame_left, from_=5, to=min(
        CURRENT_FRAME_WIDTH, CURRENT_FRAME_HEIGHT), number_of_steps=min(CURRENT_FRAME_WIDTH, CURRENT_FRAME_HEIGHT))
    sld2_d.set(init2_d_px)
    sld2_d.pack(fill="x", pady=(0, 8))

    def on_x2(val):
        global TARGET2_REL_X
        x_px = int(float(val))
        TARGET2_REL_X = max(0.0, min(1.0, x_px / max(1, CURRENT_FRAME_WIDTH)))
        val2_x.set(f"X: {x_px}")

    def on_y2(val):
        global TARGET2_REL_Y
        y_px = int(float(val))
        TARGET2_REL_Y = max(0.0, min(1.0, y_px / max(1, CURRENT_FRAME_HEIGHT)))
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
    ctk.CTkLabel(frame_left, text="").pack(pady=(8, 0))

    # Rendering settings (right column)
    lblr_title = ctk.CTkLabel(frame_right, text="Rendering")
    lblr_title.pack(anchor="w", pady=(0, 6))

    # Deadband is now fixed via settings (default 1 px); removed from GUI

    # Mask toggle
    mask_var = tk.BooleanVar(value=SHOW_MASK)
    chk_mask = ctk.CTkCheckBox(
        frame_right, text="Show red mask", variable=mask_var)
    chk_mask.pack(anchor="w", pady=(4, 8))

    def on_mask_toggle():
        global SHOW_MASK
        SHOW_MASK = bool(mask_var.get())

    chk_mask.configure(command=on_mask_toggle)

    # Reset to defaults button (visual + detection)
    def on_reset_defaults():
        global DEADBAND_PX, HOUGH_PARAM2, MIN_RADIUS, SHOW_MASK
        global STABILITY_FRAMES, ON_FRAMES, OFF_FRAMES, APPEAR_FRAMES, HOLD_FRAMES
        DEADBAND_PX = DEFAULT_DEADBAND_PX
        HOUGH_PARAM2 = DEFAULT_HOUGH_PARAM2
        MIN_RADIUS = DEFAULT_MIN_RADIUS
        SHOW_MASK = False
        STABILITY_FRAMES = DEFAULT_STABILITY_FRAMES
        ON_FRAMES = 1
        OFF_FRAMES = max(1, STABILITY_FRAMES)
        APPEAR_FRAMES = 1
        HOLD_FRAMES = max(1, STABILITY_FRAMES * 2)
        # Update GUI controls
        sld_minr.set(MIN_RADIUS)
        val_minr.set(f"Min radius: {MIN_RADIUS} px")
        mask_var.set(False)
        try:
            sld_stab.set(STABILITY_FRAMES)
            val_stab.set(f"Stability frames: {STABILITY_FRAMES}")
        except Exception:
            pass
        try:
            save_settings()
        except Exception:
            pass

    btn_reset = ctk.CTkButton(
        frame_right, text="Reset to Defaults", command=on_reset_defaults)
    btn_reset.pack(anchor="w", pady=(0, 8))

    # Detection tuning
    lbld_title = ctk.CTkLabel(frame_right, text="Detection Tuning")
    lbld_title.pack(anchor="w", pady=(8, 6))

    # Hough param2 fixed via settings (default 8); removed from GUI

    val_minr = tk.StringVar(value=f"Min radius: {MIN_RADIUS} px")
    lbl_minr = ctk.CTkLabel(frame_right, textvariable=val_minr)
    lbl_minr.pack(anchor="w")
    sld_minr = ctk.CTkSlider(frame_right, from_=2, to=30, number_of_steps=28)
    sld_minr.set(MIN_RADIUS)
    sld_minr.pack(fill="x", pady=(0, 8))

    def on_param2(val):
        pass

    def on_minr(val):
        global MIN_RADIUS
        MIN_RADIUS = int(float(val))
        val_minr.set(f"Min radius: {MIN_RADIUS} px")

    # removed param2 slider hookup
    sld_minr.configure(command=on_minr)

    # Unified Stability (temporal filtering) control
    lbl_stab = ctk.CTkLabel(frame_right, text="Stability")
    lbl_stab.pack(anchor="w", pady=(8, 6))

    val_stab = tk.StringVar(value=f"Stability frames: {STABILITY_FRAMES}")
    lbl_stabv = ctk.CTkLabel(frame_right, textvariable=val_stab)
    lbl_stabv.pack(anchor="w")
    sld_stab = ctk.CTkSlider(frame_right, from_=0, to=10, number_of_steps=10)
    sld_stab.set(STABILITY_FRAMES)
    sld_stab.pack(fill="x", pady=(0, 8))

    def on_stability(val):
        global STABILITY_FRAMES, ON_FRAMES, OFF_FRAMES, APPEAR_FRAMES, HOLD_FRAMES
        STABILITY_FRAMES = int(float(val))
        ON_FRAMES = 1
        OFF_FRAMES = max(1, STABILITY_FRAMES)
        APPEAR_FRAMES = 1
        HOLD_FRAMES = max(1, STABILITY_FRAMES * 2)
        val_stab.set(f"Stability frames: {STABILITY_FRAMES}")

    sld_stab.configure(command=on_stability)

    # Camera resolution selection
    lbl_cam = ctk.CTkLabel(frame_right, text="Camera")
    lbl_cam.pack(anchor="w", pady=(8, 6))
    res_options = ["640x480", "1280x720", "1920x1080"]
    cur_res = f"{FRAME_WIDTH}x{FRAME_HEIGHT}"
    if cur_res not in res_options:
        res_options.insert(0, cur_res)
    res_var = tk.StringVar(value=cur_res)

    def on_res_change(choice: str):
        try:
            w_s, h_s = choice.split("x")
            w_n = int(w_s)
            h_n = int(h_s)
        except Exception:
            return
        global FRAME_WIDTH, FRAME_HEIGHT
        FRAME_WIDTH = w_n
        FRAME_HEIGHT = h_n
        # Persist desired resolution; camera thread will apply dynamically
        try:
            save_settings()
        except Exception:
            pass

    opt_res = ctk.CTkOptionMenu(
        frame_right, values=res_options, variable=res_var, command=on_res_change)
    opt_res.pack(anchor="w")

    # Status line for current actual resolution and FPS
    status_var = tk.StringVar(
        value=f"Actual: {CURRENT_FRAME_WIDTH}x{CURRENT_FRAME_HEIGHT} @ {CURRENT_FPS:.1f} fps")
    lbl_status = ctk.CTkLabel(frame_right, textvariable=status_var)
    lbl_status.pack(anchor="w", pady=(6, 0))

    # --- Detection Mode Toggle ---
    mode_var = tk.BooleanVar(value=bool(USE_FAST_DETECTION))

    def on_mode_toggle():
        global USE_FAST_DETECTION
        USE_FAST_DETECTION = mode_var.get()
        mode_label = "FAST (Contours)" if USE_FAST_DETECTION else "HUGHES (Hough Circles)"
        print(f"[INFO] Detection mode switched to: {mode_label}")
        # Save this setting so it persists across runs
        save_settings()

    chk_mode = ctk.CTkSwitch(
        frame_right,
        text="Detection Mode: FAST / HUGHES",
        variable=mode_var,
        command=on_mode_toggle,
    )
    chk_mode.pack(anchor="w", pady=(8, 0))

    def _update_status():
        status_var.set(
            f"Actual: {CURRENT_FRAME_WIDTH}x{CURRENT_FRAME_HEIGHT} @ {CURRENT_FPS:.1f} fps")
        root.after(500, _update_status)

    root.after(600, _update_status)

    # Dynamically sync slider ranges with actual camera resolution
    last_w = CURRENT_FRAME_WIDTH
    last_h = CURRENT_FRAME_HEIGHT

    def _sync_ranges():
        nonlocal last_w, last_h
        w = CURRENT_FRAME_WIDTH
        h = CURRENT_FRAME_HEIGHT
        if w != last_w or h != last_h:
            sld1_x.configure(to=w, number_of_steps=max(1, w))
            sld1_y.configure(to=h, number_of_steps=max(1, h))
            sld1_d.configure(to=min(w, h), number_of_steps=max(1, min(w, h)))
            sld2_x.configure(to=w, number_of_steps=max(1, w))
            sld2_y.configure(to=h, number_of_steps=max(1, h))
            sld2_d.configure(to=min(w, h), number_of_steps=max(1, min(w, h)))

            x1 = int(TARGET1_REL_X * w)
            y1 = int(TARGET1_REL_Y * h)
            x2 = int(TARGET2_REL_X * w)
            y2 = int(TARGET2_REL_Y * h)
            sld1_x.set(x1)
            val1_x.set(f"X: {x1}")
            sld1_y.set(y1)
            val1_y.set(f"Y: {y1}")
            sld2_x.set(x2)
            val2_x.set(f"X: {x2}")
            sld2_y.set(y2)
            val2_y.set(f"Y: {y2}")

            last_w, last_h = w, h

        root.after(250, _sync_ranges)

    root.after(300, _sync_ranges)

    def on_close():
        stop_event.set()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


def main():
    # Load persisted settings (if available)
    load_settings()

    # Initialize PLC writer (optional)
    if _PLC_AVAILABLE:
        try:
            plc_init_default()
        except Exception:
            pass
    else:
        if _PLC_IMPORT_ERROR is not None:
            print(f"PLC disabled: {_PLC_IMPORT_ERROR}")

    # Start camera processing in a background thread
    cam_thread = threading.Thread(
        target=run_camera, args=(_stop_event,), daemon=True)
    cam_thread.start()

    # Start the GUI (blocks until closed)
    start_gui(_stop_event)

    # Ensure camera thread ends
    _stop_event.set()
    cam_thread.join(timeout=1.0)

    # Shutdown PLC writer
    if _PLC_AVAILABLE:
        try:
            plc_shutdown_default()
        except Exception:
            pass


if __name__ == "__main__":
    main()
