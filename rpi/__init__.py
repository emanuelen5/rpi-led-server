from util import is_raspberry_pi

if not is_raspberry_pi():
    # Replace libraries by fake ones
    import sys
    import fake_rpi

    sys.modules['RPi'] = fake_rpi.RPi  # Fake RPi
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO  # Fake GPIO
    sys.modules['smbus'] = fake_rpi.smbus  # Fake smbus (I2C)

from RPi import GPIO

__all__ = ["GPIO"]
