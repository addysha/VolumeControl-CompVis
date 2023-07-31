import cv2 as cv2
import pyautogui
import mediapipe as mp

capture = cv2.VideoCapture(0)
mp_hads = mp.solutions.hands
hands= mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                      min_detection_confidence=0.5,min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

while True:
    ret,frame = cap.read()
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BAYER_BG2BGR)

    results = hands.process(image_rgb)