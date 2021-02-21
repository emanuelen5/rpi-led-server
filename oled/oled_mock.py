import cv2
import numpy as np
from dataclasses import dataclass, field
import sys

DISPLAY_SIZE = (64, 96, 3)


@dataclass
class Display:
    buffer: np.ndarray = field(default_factory=lambda: np.zeros(DISPLAY_SIZE, dtype=np.float32))

    def clear(self):
        self.buffer = np.zeros(DISPLAY_SIZE)

    def string(self, x, y, s: str, color=(1., 1., 1.)):
        cv2.putText(self.buffer, s, (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.25, color)

    def display(self):
        cv2.imshow("SSD1331", cv2.resize(self.buffer, fx=3., fy=3., dsize=None))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sys.exit(0)


class OLED:
    def __enter__(self) -> Display:
        self.open()
        d = Display()
        return d

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @staticmethod
    def open():
        pass

    @staticmethod
    def close():
        pass
