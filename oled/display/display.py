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

    def string(self, x, y, s: str, color=(1., 1., 1.)):
        cv2.putText(self.buffer, s, (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.25, color)

    def display(self):
        self.buffer[self.buffer < 0] = 0
        self.buffer[self.buffer > 1.0] = 1.0
        liboled.display(self.buffer)

    def open(self):
        liboled.init()

    @staticmethod
    def close():
        liboled.deinit()


@dataclass
class OpenCVDisplay(Display):
    displayed: bool = False
    scaling: float = 6.0

    def __post_init__(self):
        # Pre-compute grid
        scaled_buffer = cv2.resize(self.buffer, fx=self.scaling, fy=self.scaling, dsize=None)
        y, x, z = scaled_buffer.shape
        X, Y, _ = np.meshgrid(range(x), range(y), range(z))
        self.grid = (Y % self.scaling == self.scaling - 1) | (X % self.scaling == self.scaling - 1)

    def display(self):
        super().display()
        buffer = liboled.get_buffer().astype(np.float32)
        buffer[:, :, 0] = buffer[:, :, 0] * 1.0 / 0xF8
        buffer[:, :, 1] = buffer[:, :, 1] * 1.0 / 0xFC
        buffer[:, :, 2] = buffer[:, :, 2] * 1.0 / 0xF8
        buffer = cv2.resize(buffer, fx=self.scaling, fy=self.scaling, dsize=None, interpolation=cv2.INTER_NEAREST)
        # Make grid
        buffer[self.grid] = 0.1 + buffer[self.grid] * 0.9
        # Make border
        buffer = cv2.copyMakeBorder(buffer, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=(1., 1., 1.))
        cv2.imshow("OLED_Display", buffer)
        if not self.displayed:
            self.displayed = True
            print("Press q to exit")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sys.exit(0)