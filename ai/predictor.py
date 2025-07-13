import cv2
import mediapipe as mp
import pickle
import numpy as np

MODEL_PATH = "assets/trained_models/gesture_svm.pkl"

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Load the trained SVM model
with open(MODEL_PATH, "rb") as f:
    clf = pickle.load(f)

def flatten_landmarks(landmarks):
    return [coord for lm in landmarks for coord in (lm.x, lm.y, lm.z)]

def predict_gesture(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        lm = results.multi_hand_landmarks[0].landmark
        features = flatten_landmarks(lm)
        prediction = clf.predict([features])
        return prediction[0], results.multi_hand_landmarks[0]
    else:
        return None, None

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open webcam.")
        exit(1)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        gesture, landmarks = predict_gesture(frame)

        if landmarks:
            mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

        if gesture:
            cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Gesture Prediction", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
