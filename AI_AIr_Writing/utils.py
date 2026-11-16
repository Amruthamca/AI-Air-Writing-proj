
import cv2


def show_text(frame, text, position, color=(255, 255, 255)):
    cv2.putText(
        frame,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2
    )


def show_controls(frame):
    controls = [
        "INDEX FINGER: DRAW",
        "TWO FINGERS: STOP",
        "C: CLEAR",
        "S: SAVE",
        "1-4: CHANGE COLOR",
        "+ / -: BRUSH SIZE",
        "Q: QUIT"
    ]

    for i, text in enumerate(controls):
        show_text(frame, text, (20, 30 + i * 30))
