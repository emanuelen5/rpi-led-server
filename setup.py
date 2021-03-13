from distutils.core import setup, Extension
import numpy
from rpi import is_raspberry_pi

if is_raspberry_pi():
    module = Extension(
        'liboled',
        sources=[
            'oled/liboled.c',
            'oled/ssd1331.c',
        ],
        include_dirs=["oled", numpy.get_include()],
        extra_compile_args=["-Ofast", "-march=native"],
        libraries=['bcm2835'],
    )
else:
    module = Extension(
        'liboled',
        sources=[
            'oled/liboled.c',
            'oled/ssd1331.c',
        ],
        include_dirs=["oled", "oled/mocks", numpy.get_include()],
        extra_compile_args=["-Ofast", "-march=native"],
    )

setup(
    name='oled',
    version='0.1.0',
    description='Python wrapper for controlling an SSD1331 OLED display from a Raspberry Pi',
    author='Erasmus Cedernaes',
    author_email='erasmus.cedernaes@gmail.com',
    url='https://github.com/emanuelen5/rpi-led-server/',
    long_description='Python wrapper for controlling an OLED display',
    ext_modules=[module]
)
