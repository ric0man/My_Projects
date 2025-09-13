import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os
from collections import deque

# Load trained model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'mask_detector.keras')
model = load_model(model_path)

# Load Haarcascade face detector
cascade_path = os.path.join(BASE_DIR, 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(cascade_path)

if face_cascade.empty():
    raise IOError("Failed to load Haarcascade XML file. Check the path or file integrity.")

# Initialize webcam
cap = cv2.VideoCapture(0)
prediction_history = deque(maxlen=5)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=7)

    for (x, y, w, h) in faces:
        if w < 50 or h < 50:
            continue  # Skip tiny detections

        face_img = gray[y:y+h, x:x+w]
        face_input = cv2.resize(face_img, (100, 100)) / 255.0
        face_input = face_input.reshape(1, 100, 100, 1)

        pred = model.predict(face_input)
        confidence = np.max(pred)
        label = np.argmax(pred)

        if confidence < 0.85:
            label_text = "Uncertain"
            color = (255, 255, 0)
        else:
            label_text = "Mask" if label == 1 else "No Mask"
            color = (0, 255, 0) if label == 1 else (0, 0, 255)

        prediction_history.append(label)
        smoothed_label = round(np.mean(prediction_history))

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, f"{label_text} ({confidence:.2f})", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow('Face Mask Detection', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()