
from flask import Flask, render_template, request, jsonify
import cv2
import base64
import numpy as np
import mediapipe as mp

app = Flask(__name__)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
rectangle = None
mask = None
back_area = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset', methods=['GET'])
def reset():
    global rectangle, mask, back_area
    rectangle = None
    mask = None
    back_area = 0
    return jsonify(success=True)

@app.route('/set_rectangle', methods=['POST'])
def set_rectangle():
    global rectangle, back_area, mask
    data = request.json
    x1 = int(data['x1'])
    y1 = int(data['y1'])
    x2 = int(data['x2'])
    y2 = int(data['y2'])
    rectangle = (x1, y1, x2, y2)
    back_area = (x2 - x1) * (y2 - y1)
    mask = None 
    return jsonify(success=True)

@app.route('/process_frame', methods=['POST'])
def process_frame():
    global mask, rectangle, back_area
    data = request.json['image']
    img_data = base64.b64decode(data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    h, w, _ = img.shape
    if rectangle and mask is None:
        mask = np.zeros((h, w), dtype=np.uint8)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        if rectangle:
            points = np.array([[int(lm.x * w), int(lm.y * h)] for lm in hand_landmarks.landmark], dtype=np.int32)
            if len(points) >= 3:
                hull = cv2.convexHull(points)
                temp_mask = np.zeros((h, w), dtype=np.uint8)
                cv2.fillConvexPoly(temp_mask, hull, 255)
                x1, y1, x2, y2 = rectangle
                roi_temp = temp_mask[y1:y2, x1:x2]
                roi_mask = mask[y1:y2, x1:x2]
                roi_mask[roi_temp > 0] = 255

    if rectangle:
        x1, y1, x2, y2 = rectangle
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
    if mask is not None:
        alpha = 0.5
        overlay_color = (200, 200, 200) 
        indices = np.where(mask == 255)
        if len(indices[0]) > 0:
            touched_pixels = img[indices[0], indices[1]]
            overlay_pixels = np.full(touched_pixels.shape, overlay_color, dtype=np.uint8)
            blended = cv2.addWeighted(touched_pixels, 1 - alpha, overlay_pixels, alpha, 0)
            img[indices[0], indices[1]] = blended

    coverage = (np.count_nonzero(mask) / back_area * 100) if back_area > 0 and mask is not None else 0
    _, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    annotated = 'data:image/jpeg;base64,' + jpg_as_text

    return jsonify(coverage=coverage, annotated=annotated)

if __name__ == '__main__':
    app.run(debug=True)
