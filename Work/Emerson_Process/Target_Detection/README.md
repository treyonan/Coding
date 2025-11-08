Target Detection (OpenCV + CustomTkinter)

Overview
- Live camera feed (default camera index: 1)
- Detects up to two red circles per frame
  - HSV threshold + morphology + HoughCircles
  - Circle-only validation via circularity and fill ratio
  - Multi-scale fallback (2× upsample) to recover tiny far circles
- Two configurable target circles overlaid on the frame
  - Sliders for X, Y, and Diameter (pixels) for Target 1 and Target 2
  - Labels at top-left turn green when any circle center lies inside the target (with hysteresis)
- Visual smoothing
  - Deadband slider controls drawn center stability (px)
  - Hit logic uses hysteresis based on the same deadband to avoid flicker
  - Dynamic outline thickness scales with circle size
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
- `settings.json` — persisted settings (camera, frame, targets, deadband)

Settings Persistence
- On start, the app loads `settings.json` if present.
- On exit (pressing 'q' or closing GUI), the app saves current settings.
- Stored fields:
  - `camera_index`, `frame_width`, `frame_height`
  - `deadband_px`
  - `target1`: `{ x, y, diameter }` in pixels
  - `target2`: `{ x, y, diameter }` in pixels

Controls (GUI)
- Target 1 / Target 2: X, Y, Diameter sliders in pixel units of the current frame.
- Rendering: Deadband slider sets both visual center deadband and hit hysteresis band.

Tuning & Notes
- If circles are very small (camera far away), the multi-scale fallback and dynamic outline thickness help visibility.
- For even better detail at distance, increase `frame_width`/`frame_height` in `settings.json` (e.g., 1280×720) if supported by your camera.
- Targets store internal positions relatively, so changing resolution keeps positions coherent.

Planned / Optional
- Add on-GUI Quit button.
- Expose detection sensitivity (Hough `param2`, `minRadius`) as GUI sliders.
- PLC integration: write BOOL tags for Target1/2 hit states (module scaffold in `src/utils/pylogix.py`).
