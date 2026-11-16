
import cv2

from hand_tracking import HandTracker
from drawing import AirDrawing
from utils import show_controls, show_text


# Initialize our project
tracker = HandTracker()
drawing = AirDrawing()

# Available pen colours (BGR format)
colors = {
    1: (255, 0, 255),   # Pink
    2: (0, 255, 0),     # Green
    3: (255, 0, 0),     # Blue
    4: (0, 255, 255)    # Yellow
}

# Start webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Webcam not found!")
    exit()

print("AI Air Writing Started!")

while True:

    success, frame = cap.read()

    if not success:
        print("Cannot read webcam!")
        break

    # Flip webcam image
    frame = cv2.flip(frame, 1)

    height, width, _ = frame.shape

    # Detect hand
    frame = tracker.find_hands(frame)

    # Get finger positions
    landmarks = tracker.get_landmarks(frame)

    if landmarks:

        # Index finger and middle finger positions
        index_tip = landmarks[8]
        index_joint = landmarks[6]

        middle_tip = landmarks[12]
        middle_joint = landmarks[10]

        # Detect finger gestures
        index_up = index_tip[2] < index_joint[2]
        middle_up = middle_tip[2] < middle_joint[2]

        if index_up and not middle_up:

            x = index_tip[1]
            y = index_tip[2]

            drawing.draw(x, y)

            cv2.circle(frame, (x, y), 10, drawing.color, cv2.FILLED)

        else:
            drawing.stop_drawing()

    else:
        drawing.stop_drawing()

    # Resize drawing canvas to webcam size
    canvas = cv2.resize(drawing.canvas, (width, height))

    # Combine webcam and drawing
    frame = cv2.addWeighted(frame, 1, canvas, 0.8, 0)

    # Display controls
    show_controls(frame)

    show_text(frame, "AI AIR WRITING", (width - 300, 40), (0, 255, 255))

    # Keyboard controls

    cv2.imshow("AI Air Writing", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    elif key == ord('c'):
        drawing.clear()

    elif key == ord('s'):
        drawing.save()

    elif key in (ord('1'), ord('2'), ord('3'), ord('4')):
        drawing.change_color(colors[int(chr(key))])
        print("Color changed!")

    elif key in (ord('+'), ord('=')):
        drawing.change_brush_size(drawing.brush_size + 1)

    elif key in (ord('-'), ord('_')):
        drawing.change_brush_size(drawing.brush_size - 1)


# Close everything
cap.release()
cv2.destroyAllWindows()
