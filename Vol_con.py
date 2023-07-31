import cv2 as cv2
import pyautogui
import mediapipe as mp

# Open the default camera (index 0) to capture video
cap = cv2.VideoCapture(0)

# Initialize the Mediapipe Hands model with desired parameters
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                      min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB format as Mediapipe works with RGB images
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with the Mediapipe Hands model to detect hands and landmarks
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks and connections on the frame using Mediapipe's drawing utilities
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the y-coordinate of the index finger tip and thumb tip landmarks
            index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            thumb_y =  hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

            # Determine the hand gesture based on the relative positions of the index finger and thumb
            if index_finger_y < thumb_y:
                hand_gesture = 'pointing up'
            elif index_finger_y > thumb_y:
                hand_gesture = 'pointing down'
            else:
                hand_gesture = 'other'

            # Perform the corresponding action based on the hand gesture
            if hand_gesture == 'pointing up':
                pyautogui.press('volumeup')
            elif hand_gesture == 'pointing down':
                pyautogui.press('volumedown')

    # Display the frame with the detected hand landmarks and the hand gesture text
    cv2.imshow('Hand Gesture', frame)

    # Exit the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
