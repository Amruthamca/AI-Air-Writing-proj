
import cv2
import numpy as np


class AirDrawing:

    def __init__(self, width=1280, height=720):
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)

        self.color = (255, 0, 255)
        self.brush_size = 5

        self.previous_x = 0
        self.previous_y = 0

    def draw(self, x, y):

        if self.previous_x != 0 and self.previous_y != 0:
            cv2.line(
                self.canvas,
                (self.previous_x, self.previous_y),
                (x, y),
                self.color,
                self.brush_size
            )

        self.previous_x = x
        self.previous_y = y

    def stop_drawing(self):
        self.previous_x = 0
        self.previous_y = 0

    def clear(self):
        self.canvas[:] = 0
        self.stop_drawing()

    def change_color(self, color):
        self.color = color

    def change_brush_size(self, size):
        self.brush_size = max(1, min(size, 30))

    def save(self):
        cv2.imwrite("air_writing.png", self.canvas)
        print("Drawing saved successfully!")
