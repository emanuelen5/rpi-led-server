import cv2
import numpy as np
from typing import List, Tuple, Union
from dataclasses import dataclass, field
from adafruit_pypixelbuf import PixelBuf


ND_LIKE = Union[Tuple[int, int, int], List[int], np.ndarray]


@dataclass
class LED_Model(PixelBuf):
    pixel_count: int
    buffer: np.ndarray = field(init=False, repr=False)

    def __post_init__(self):
        self.buffer = np.zeros((self.pixel_count, 3), np.uint8)

    def __len__(self):
        return self.pixel_count

    def __getitem__(self, item: int):
        return self.buffer[item]

    def __setitem__(self, key: int, value: ND_LIKE):
        self.buffer[key] = value

    def __iter__(self):
        return (px for px in self.buffer)

    def fill(self, value: ND_LIKE):
        for i in range(len(self)):
            self[i] = value

    def show(self):
        pass


@dataclass
class LED_ModelView(LED_Model):
    brightness: float = 1.0
    scale: Tuple[int, int] = (6, 6)

    def __post_init__(self):
        super().__post_init__()
        self.frame_buffer = np.zeros((self.scale[0], self.scale[1] * self.pixel_count, 3), dtype=np.float32)

    def show(self):
        self.refresh()

    def refresh(self):
        for i in range(len(self)):
            self.frame_buffer[:, i*self.scale[1]:(i+1)*self.scale[1]] = self[i]
        self.frame_buffer *= self.brightness
        cv2.imshow("led_view", self.frame_buffer / 255)


def create_pixels(num_pixels: int = 50, brightness: float = 1.0, scale: Tuple[int, int] = (200, 20), *args, **kwargs):
    return LED_ModelView(num_pixels, brightness=brightness, scale=scale)
