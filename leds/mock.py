import numpy as np
from typing import List, Tuple, Union
from dataclasses import dataclass
from adafruit_pypixelbuf import PixelBuf
from .model import LED_BaseModel


ND_LIKE = Union[Tuple[int, int, int], List[int], np.ndarray]


@dataclass
class LED_Model(PixelBuf, LED_BaseModel):
    pixel_count: int
    brightness: float = 1.0

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


def create_pixels(num_pixels: int = 50, brightness: float = 1.0, *args, **kwargs):
    return LED_Model(num_pixels, brightness=brightness)
