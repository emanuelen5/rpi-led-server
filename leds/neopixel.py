# Simple test for NeoPixels on Raspberry Pi
import board
from neopixel import GRB, NeoPixel


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = GRB


def create_pixels(num_pixels: int = 50, brightness: float = 0.1, pin=pixel_pin, order=ORDER, **kwargs):
    return NeoPixel(
        pin, num_pixels, brightness=brightness, auto_write=False, pixel_order=order, **kwargs
    )
