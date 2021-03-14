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
        assert 0 <= item < self.pixel_count
        return self.buffer[item]

    def __setitem__(self, key: int, value: ND_LIKE):
        assert isinstance(key, int)
        assert 0 <= key < self.pixel_count
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
    scale: float = 1.0

    def show(self):
        self.refresh()

    def refresh(self):
        disp = np.zeros((int(self.scale), int(self.scale * len(self.buffer)), 3), dtype=np.float32)
        for i in range(len(self)):
            px = self[i]
            disp[:, int(i*self.scale):int((i+1)*self.scale)] = px
        disp *= self.brightness
        cv2.imshow("led_view", disp)


def create_pixels(num_pixels: int = 50, brightness: float = 0.1, scale: float = 6, *args, **kwargs):
    return LED_ModelView(num_pixels, brightness=brightness, scale=scale)
