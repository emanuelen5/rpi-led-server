from rpi import is_raspberry_pi
from .rotary_encoder import PINS

if is_raspberry_pi():
    from .rotary_encoder import RotaryEncoder
else:
    from .rotary_encoder import RotaryEncoderMock as RotaryEncoder

__all__ = ["RotaryEncoder", "PINS"]
