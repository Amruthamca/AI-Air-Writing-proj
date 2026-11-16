
import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

canvas = None
previous_x, previous_y = 0, 0

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    if canvas is None:
        canvas = np.zeros((h, w, c), dtype=np.uint8)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    drawing = False

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

            lm = hand_landmarks.landmark

            index_up = lm[8].y < lm[6].y
            middle_up = lm[12].y < lm[10].y


            if index_up and not middle_up:
                drawing = True

                x = int(lm[8].x * w)
                y = int(lm[8].y * h)

                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

                if previous_x != 0 and previous_y != 0:
                    cv2.line(
                        canvas,
                        (previous_x, previous_y),
                        (x, y),
                        (255, 0, 255),
                        5
                    )

                previous_x, previous_y = x, y

            else:
                previous_x, previous_y = 0, 0

    else:
        previous_x, previous_y = 0, 0

    status = "DRAWING" if drawing else "STOPPED"

    combined = cv2.add(frame, canvas)

    cv2.putText(
        combined, status, (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX, 1,
        (0, 255, 0) if drawing else (0, 0, 255), 2
    )

    cv2.putText(
        combined, "C: Clear | Q: Quit",
        (20, 80), cv2.FONT_HERSHEY_SIMPLEX,
        0.7, (255, 255, 255), 2
    )

    cv2.imshow("AI Air Writing", combined)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        canvas = np.zeros((h, w, c), dtype=np.uint8)

    if key == ord('s'):
        cv2.imwrite("air_writing.png", canvas)
        print("Drawing saved successfully!")

    if key == ord('q'):
        break

cap.release()
hands.close()
cv2.destroyAllWindows()
