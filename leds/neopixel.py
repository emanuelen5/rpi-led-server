# Simple test for NeoPixels on Raspberry Pi
import board
from typing import Union, Tuple, List
from neopixel import GRB, NeoPixel
import numpy as np
from .model import LED_BaseModel


ND_LIKE = Union[Tuple[int, int, int], List[int], np.ndarray]


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = GRB


class LED_Model(NeoPixel, LED_BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buffer = np.zeros((len(self), 3), np.uint8)

    def __getitem__(self, item: int):
        return self.buffer[item]

    def __setitem__(self, key: int, value: ND_LIKE):
        super().__setitem__(key, value)
        self.buffer[key] = value

    def __iter__(self):
        return (px for px in self.buffer)

    def fill(self, value: ND_LIKE):
        super().fill(value)
        for i in range(len(self)):
            self[i] = value


def create_pixels(num_pixels: int = 50, brightness: float = 0.1, pin=pixel_pin, order=ORDER, **kwargs):
    return NeoPixel(
        pin, num_pixels, brightness=brightness, auto_write=False, pixel_order=order, **kwargs
    )
