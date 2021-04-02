from rpi import is_raspberry_pi
from .rotary_encoder import PINS

if is_raspberry_pi():
    from .rotary_encoder import RotaryEncoderGPIOModel as RotaryEncoder
else:
    from .rotary_encoder import RotaryEncoderView as RotaryEncoder

__all__ = ["RotaryEncoder", "PINS"]
