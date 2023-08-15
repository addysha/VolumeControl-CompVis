import cv2
import pyautogui
import mediapipe as mp

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                      min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

while True:
    ret, frame = cap.read()
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Check if the hand is in a peace sign (Custom gesture: Thumb above knuckles below the tips of ring and pinky)
            knuckle_below_ring_pinky = all(hand_landmarks.landmark[i].y < hand_landmarks.landmark[i+1].y for i in [17, 19])
            thumb_above_knuckles = hand_landmarks.landmark[4].y < hand_landmarks.landmark[17].y and hand_landmarks.landmark[4].y < hand_landmarks.landmark[19].y

            is_peace_sign = knuckle_below_ring_pinky and thumb_above_knuckles

            # Mute the volume if a peace sign gesture is detected
            if is_peace_sign:
                pyautogui.press('volumemute')
            else:
                index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

                if index_finger_y < thumb_y:
                    hand_gesture = 'pointing up'
                elif index_finger_y > thumb_y:
                    hand_gesture = 'pointing down'
                else:
                    hand_gesture = 'other'

                if hand_gesture == 'pointing up':
                    pyautogui.press('volumeup')
                elif hand_gesture == 'pointing down':
                    pyautogui.press('volumedown')

    cv2.imshow('Hand Gesture', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
