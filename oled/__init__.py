from util import is_raspberry_pi

if is_raspberry_pi():
    from .oled import OLED
else:
    from oled.mocks.oled import OLED
