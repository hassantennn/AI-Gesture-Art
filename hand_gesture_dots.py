import pygame
import cv2
import mediapipe as mp
from ai.predictor import predict_gesture
import sys
import math
import colorsys
import random

# --- Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Reactive Dot Grid with Gestures")
clock = pygame.time.Clock()

# --- Grid and Dot settings
SPACING = 5
BASE_RADIUS = 1
REACT_RADIUS = 40
MAX_ALPHA = 200
FADE_SPEED = 3  # slower fade for smooth trail

# --- Neon pastel color generator (HSV to RGB) with high saturation and brightness
def neon_color_from_hue(hue):
    saturation = 0.9
    brightness = 1.0
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, brightness)
    return (int(r * 255), int(g * 255), int(b * 255))

# --- Dot class with neon glow effect
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BASE_RADIUS
        self.alpha = 0
        self.color = (100, 255, 255)  # default neon-ish color (cyan)
        self.active = False

    def update(self, hand_pos, active_color):
        dx = self.x - hand_pos[0]
        dy = self.y - hand_pos[1]
        dist_sq = dx * dx + dy * dy

        if dist_sq < REACT_RADIUS * REACT_RADIUS:
            self.active = True
            self.alpha = MAX_ALPHA
            if self.color != active_color:
                self.color = active_color
            self.radius = BASE_RADIUS + 1.5
        else:
            if self.alpha > 0:
                self.alpha = max(0, self.alpha - FADE_SPEED)
            self.radius = BASE_RADIUS
            self.active = False

    def draw(self, surface):
        if self.alpha <= 0:
            return
        
        glow_radius = int(self.radius * 4)
        glow_surf = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
        glow_color = (*self.color[:3], int(self.alpha * 0.15))
        pygame.draw.circle(glow_surf, glow_color, (glow_radius, glow_radius), glow_radius)
        
        dot_surf = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
        dot_color = (*self.color[:3], int(self.alpha))
        pygame.draw.circle(dot_surf, dot_color, (int(self.radius * 2), int(self.radius * 2)), int(self.radius))

        surface.blit(glow_surf, (self.x - glow_radius, self.y - glow_radius))
        surface.blit(dot_surf, (self.x - self.radius * 2, self.y - self.radius * 2))

# --- Create dot grid
dots = [Dot(x, y) for x in range(0, WIDTH, SPACING) for y in range(0, HEIGHT, SPACING)]

# --- State variables
index_finger_pos = (-9999, -9999)
hue_step = 0.07
current_hue = random.random()
current_color = neon_color_from_hue(current_hue)

# --- Initialize webcam (only for cv2 video capture)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERROR: Could not open webcam.")
    sys.exit(1)

running = True
while running:
    screen.fill((10, 10, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ret, frame = cap.read()
    if not ret:
        continue
    frame = cv2.flip(frame, 1)

    # --- Get gesture prediction & hand landmarks from predictor
    gesture, landmarks = predict_gesture(frame)

    if landmarks:
        # Extract index finger tip position normalized (0-1)
        index_lm = landmarks.landmark[8]
        index_finger_pos = (int(index_lm.x * WIDTH), int(index_lm.y * HEIGHT))
    else:
        index_finger_pos = (-9999, -9999)

    # Change neon color based on gesture
    if gesture == "fist":
        current_hue = (current_hue + hue_step * 0.5) % 1.0
        current_color = neon_color_from_hue(current_hue)
    elif gesture == "peace":
        current_hue = (current_hue + hue_step * 2) % 1.0
        current_color = neon_color_from_hue(current_hue)
    elif gesture == "thumbs_up":
        current_color = (0, 255, 100)
    elif gesture == "open":
        current_color = (100, 200, 255)
    else:
        current_color = (100, 255, 255)

    # Update & draw dots
    for dot in dots:
        dot.update(index_finger_pos, current_color)
        dot.draw(screen)

    pygame.display.flip()
    clock.tick(60)

    # Show webcam with landmarks and gesture label
    if landmarks:
        mp.solutions.drawing_utils.draw_landmarks(frame, landmarks, mp.solutions.hands.HAND_CONNECTIONS)
    if gesture:
        cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Webcam Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()
