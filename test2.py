import cv2
import mediapipe as mp

lyrics = [
    "tingnan natin nang husto",
    "pagmasdan mo nang maigi",
    "ang makulay kong mundo",
    "mga tao sa paligid",
    "kahit minsa'y magulo",
    "kahit medyo alanganin",   
    "yayakapin nang buo", 
    "ikaw pa rin ang hahanapin"           
]

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    lyric_text = ""

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            finger_tips = [8, 12, 16, 20]  
            thumb_tip = 4

            fingers_up = []

            for tip in finger_tips:
                if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                    fingers_up.append(1)
                else:
                    fingers_up.append(0)

            if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 2].x:
                fingers_up.insert(0, 1)  
            else:
                fingers_up.insert(0, 0)

            total_fingers = sum(fingers_up)

            if total_fingers > 0 and total_fingers <= 5 and len(lyrics) >= total_fingers:
                lyric_text = lyrics[total_fingers - 1]

            if len(lyrics) >= 6 and fingers_up[1] == 1 and fingers_up[2] == 1 and fingers_up[3] == 0 and fingers_up[4] == 0:
                lyric_text = lyrics[5]

            if len(lyrics) >= 7 and fingers_up[1] == 1 and fingers_up[4] == 1 and fingers_up[2] == 0 and fingers_up[3] == 0:
                lyric_text = lyrics[6]

            if len(lyrics) >= 8 and total_fingers == 0:
                lyric_text = lyrics[7]

            if lyric_text:
                print(lyric_text)

    
    if lyric_text:
        cv2.putText(frame, lyric_text, (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("trip trip lang", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Esc to exit
        break

cap.release()
cv2.destroyAllWindows()
