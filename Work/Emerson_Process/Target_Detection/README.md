Target Detection (OpenCV + CustomTkinter)

Overview
- Live camera feed (default camera index: 1)
- Detects up to two red circles per frame
  - HSV threshold + morphology + HoughCircles
  - Circle-only validation via circularity and fill ratio
  - Multi-scale fallback (2x upsample) to recover tiny far circles
- Two configurable target circles overlaid on the frame
  - Sliders for X, Y, and Diameter (pixels) for Target 1 and Target 2
  - Labels at top-left turn green when any circle center lies inside the target (with hysteresis)
- Visual smoothing
  - Deadband (fixed default 1 px; configurable in settings.json)
  - Temporal stability slider reduces flicker (consecutive-frame filtering)
  - Dynamic outline thickness scales with circle size
  - Nearest-neighbor matching keeps circle identity stable across frames
- Press 'q' in the camera window to quit (also closes the GUI)
- Settings persist between runs in `settings.json`

Run
- Activate your venv
- `python src/main.py`
- Press 'q' to exit

Dependencies
- Python 3.9+
- `opencv-python`, `customtkinter`

Files
- `src/main.py` — camera processing and GUI
- `settings.json` — persisted settings (camera, frame, targets, deadband, detection)

Settings Persistence
- On start, the app loads `settings.json` if present.
- On exit (pressing 'q' or closing GUI), the app saves current settings.
- Stored fields:
  - `camera_index`, `frame_width`, `frame_height`
  - `deadband_px` (fixed in GUI; change via JSON)
  - `hough_param2` (fixed in GUI), `min_radius`
  - `stability_frames`, `show_mask`
  - `target1`: `{ x, y, diameter }` in pixels
  - `target2`: `{ x, y, diameter }` in pixels

Controls (GUI)
- Target 1 / Target 2: X, Y, Diameter sliders in pixel units of the current frame.
- Rendering: Show red mask toggle, Reset to Defaults.
- Detection Tuning: minimum radius slider.
- Camera: resolution dropdown (persistent) and live status (actual WxH @ FPS).
- Stability: single slider controlling both label debounce (delayed-off) and overlay hold time.
- Debug: checkbox to show the red mask window for tuning.

Tuning & Notes
- If circles are very small (camera far away), the multi-scale fallback and dynamic outline thickness help visibility.
- For even better detail at distance, increase `frame_width`/`frame_height` in `settings.json` (e.g., 1280x720) if supported by your camera.
- Targets store internal positions relatively, so changing resolution keeps positions coherent.
 - Slider ranges auto-sync to the actual camera resolution reported by the device.

PLC Integration (optional)
- See `src/utils/pylogix.py`. When enabled, writes debounced hit states to BOOL tags (`Target1_Hit`, `Target2_Hit`).
