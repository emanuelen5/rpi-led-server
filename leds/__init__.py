from rpi import is_raspberry_pi

if is_raspberry_pi():
    from .neopixel import LED_Model as NeoPixel, create_pixels
else:
    from .mock import LED_Model as NeoPixel, create_pixels

__all__ = ["create_pixels", "NeoPixel"]
