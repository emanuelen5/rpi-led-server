from rpi import is_raspberry_pi

if is_raspberry_pi():
    from .display import DisplayModel as Display
else:
    from .display import DisplayModelView as Display

__all__ = ["Display"]
