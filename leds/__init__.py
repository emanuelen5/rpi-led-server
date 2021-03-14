from rpi import is_raspberry_pi

if is_raspberry_pi():
    from .neopixel import NeoPixel, create_pixels
else:
    from .mock import PixelBuf as NeoPixel, create_pixels

__all__ = ["create_pixels", "NeoPixel"]
