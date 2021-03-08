from util import is_raspberry_pi

if is_raspberry_pi():
    from .display import Display
else:
    from .display import OpenCVDisplay as Display

__all__ = ["Display"]
