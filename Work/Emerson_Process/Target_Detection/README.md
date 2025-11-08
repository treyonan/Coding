Target Detection (OpenCV + CustomTkinter)

Overview
- Live camera feed (default camera index: 1)
- Detects up to one visible red circle per frame via HSV threshold + HoughCircles
- Two configurable target circles overlaid on the frame
  - Sliders for X, Y (pixels) and Diameter (pixels) in a CustomTkinter GUI
  - Target labels at top-left turn green when the detected red circle center lies inside the target radius
- Press 'q' in the camera window to quit (also closes the GUI)
- Settings persist between runs in `settings.json`

Run
- Activate your venv
- `python src/main.py`
- Press 'q' to exit

Dependencies
- Python 3.9+
- `opencv-python`, `numpy` (implicit via OpenCV), `Pillow` (for future use), `customtkinter`

Files
- `src/main.py` — application entry with camera processing and GUI
- `settings.json` — persisted settings (camera index, frame size, and both targets)

Settings Persistence
- On start, the app loads `settings.json` if present.
- On exit (pressing 'q' or closing GUI), the app saves current settings.
- Stored fields:
  - `camera_index`, `frame_width`, `frame_height`
  - `target1`: `{ x, y, diameter }` in pixels
  - `target2`: `{ x, y, diameter }` in pixels

Notes
- X,Y sliders operate in pixel coordinates of the selected frame size.
- Targets move with the frame resolution internally, using relative positions.
- If camera index or resolution is changed, positions are reinterpreted accordingly on next run.

Next Steps / TODO
- Improve detection robustness (dynamic thresholds, morphological ops)
- Add mask/debug view toggle
- Add on-GUI quit button and load/save buttons
- Bounds validation for sliders at runtime
