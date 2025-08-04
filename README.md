# BackReachTracker
This is a simple web application built with Flask and MediaPipe that uses your webcam to track how much of your back you can touch with your hand. It captures a still image of your back, allows you to define a rectangular area, and then tracks hand movements to calculate and visualize coverage using hand landmark detection.

## Why I Made This

I created this app purely out of curiosity about my own physical flexibility—specifically, to see how much of my back I could reach with my hand. I thought I could do it a 100% but I couldn't I had a spot out of reach.:'(
It was also a challenge to myself if I could build it within a 3 hr window.

## Features

- Webcam integration for live video feed.
- 5-second countdown timer for capturing a still image of your back.
- Rectangle drawing to define the back area.
- Real-time hand tracking using MediaPipe to detect and accumulate touched areas via convex hull approximation.
- Visual feedback with grey tint overlay on covered areas and a progress bar for coverage percentage.
- Responsive UI with Bootstrap for a modern look.

## Requirements

- Python 3.x
- Flask
- OpenCV (opencv-python)
- MediaPipe
- NumPy

Install dependencies:
```
pip install flask opencv-python mediapipe numpy
```

## Usage

1. Run the application:
   ```
   python app.py
   ```

2. Open your browser and go to `http://127.0.0.1:5000/`.

3. Follow the steps:
   - **Step 1**: Click "Capture Still" for a 5-second countdown to take a photo of your back (use a mirror or position accordingly).
   - **Step 2**: Draw a rectangle on the captured image to mark your back area, then confirm.
   - **Step 3**: Move your hand over your back; the app tracks coverage in real-time with a tint overlay and progress bar.
   - Click "Reset" to start over.

Note: Ensure your browser allows webcam access. The feed is mirrored for natural UX.

## Limitations

- The rectangle for the back is static for the entire hand tracking duration.
- Hand tracking accuracy depends on lighting and webcam quality.
- Convex hull may slightly overestimate hand area for concave shapes (e.g., between fingers).
- High resolutions may cause latency; adjust interval in JS if needed.
- Single hand detection; I personally would recommend using dominant hand.


MIT License
