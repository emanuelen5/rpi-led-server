try:
    from RPi import GPIO
except ImportError:
    from fake_rpi.RPi import GPIO

__all__ = ["GPIO"]
