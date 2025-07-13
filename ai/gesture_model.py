import cv2
import mediapipe as mp
import csv
import os
from sklearn import svm
import pickle

GESTURE_LABELS = ["fist", "open", "peace", "thumbs_up"]
DATA_PATH = "assets/gestures"
MODEL_PATH = "assets/trained_models/gesture_svm.pkl"

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

def flatten_landmarks(landmarks):
    return [coord for lm in landmarks for coord in (lm.x, lm.y, lm.z)]

def record_gesture(label, samples=100):
    cap = cv2.VideoCapture(0)
    collected = 0
    print(f"Recording gesture: {label}")

    with open(f"{DATA_PATH}/{label}.csv", "w", newline="") as f:
        writer = csv.writer(f)

        while collected < samples:
            ret, frame = cap.read()
            if not ret:
                continue
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            if results.multi_hand_landmarks:
                lm = results.multi_hand_landmarks[0].landmark
                flat = flatten_landmarks(lm)
                writer.writerow(flat)
                collected += 1
                cv2.putText(frame, f"Collecting {label} ({collected}/{samples})", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow("Recording", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    print("Done recording.")

def train_model():
    X, y = [], []
    for label in GESTURE_LABELS:
        path = f"{DATA_PATH}/{label}.csv"
        if not os.path.exists(path):
            continue
        with open(path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                X.append([float(x) for x in row])
                y.append(label)
    clf = svm.SVC(kernel="linear")
    clf.fit(X, y)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(clf, f)
    print(f"Model trained and saved to {MODEL_PATH}")

if __name__ == "__main__":
    print("1. Record Gesture")
    print("2. Train Model")
    choice = input("Choose: ")

    if choice == "1":
        for gesture in GESTURE_LABELS:
            input(f"Press Enter to record '{gesture}'...")
            record_gesture(gesture)
    elif choice == "2":
        train_model()
    else:
        print("Invalid choice")
