import cv2 as cv2
import pyautogui
import mediapipe as mp

capture = cv2.VideoCapture(0)
mp_hads = mp.solutions.hands
hands= mp_hands.Hands(static_image_mode=False, max_num_hands=1,)