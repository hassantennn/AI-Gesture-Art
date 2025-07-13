# ✨ AI Gesture-Controlled Neon Dot Grid

An interactive art project that uses real-time **hand gesture recognition** to control a glowing **neon dot grid** — combining AI, computer vision, and creative coding.

![demo](assets/demo.gif) <!-- Replace with actual demo GIF or screenshot -->

---

## 🧠 Description

This project tracks your hand gestures using your webcam and uses them to dynamically control a glowing field of dots in real-time. You can train your own gestures and trigger different visual effects like color shifts, glow pulses, and more.

It’s a fusion of **art + machine learning + computer vision**.

---

## 🖐️ Recognized Gestures

| Gesture      | Action                                      |
|--------------|---------------------------------------------|
| Fist         | Slow color shift                            |
| Peace ✌️      | Fast color shift                            |
| Thumbs Up 👍   | Turns grid green (affirmative pulse)        |
| Open Palm 🖐️  | Calming blue glow                          |

You can train and add your own gestures too!

---

## ⚙️ How It Works

1. **MediaPipe** tracks hand landmarks in real-time from your webcam.
2. A custom **SVM model** (trained on your gesture recordings) recognizes hand gestures.
3. **Pygame** visualizes a neon dot grid that reacts to your finger position and gesture state.

