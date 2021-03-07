import numpy as np
import cv2
from dataclasses import dataclass, field
import liboled
import sys


@dataclass
class Display:
    buffer: np.ndarray = field(
        default_factory=lambda: np.zeros((liboled.OLED_HEIGHT, liboled.OLED_WIDTH, 3), dtype=np.float32))

    def clear(self):
        self.buffer[:, :, :] = 0.0
        self.display()

    def string(self, x, y, s: str, color=(1., 1., 1.)):
        cv2.putText(self.buffer, s, (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.25, color)

    def display(self):
        liboled.display(self.buffer)

    def open(self):
        liboled.init()

    @staticmethod
    def close():
        liboled.deinit()


@dataclass
class OpenCVDisplay(Display):
    displayed: bool = False

    def display(self):
        super().display()
        buffer = liboled.get_buffer()
        cv2.imshow("OLED_Display", cv2.resize(buffer, fx=3., fy=3., dsize=None, interpolation=None))
        if not self.displayed:
            self.displayed = True
            print("Press q to exit")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sys.exit(0)
