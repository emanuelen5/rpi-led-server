from distutils.core import setup, Extension

module1 = Extension(
    'oled',
    sources=[
        'oled/liboled.c',
    ],
    include_dirs=["oled"]
)

setup(
    name='oled',
    version='0.1.0',
    description='Python wrapper for controlling an OLED display',
    author='Erasmus Cedernaes',
    author_email='erasmus.cedernaes@gmail.com',
    url='https://github.com/emanuelen5/rpi-led-server/',
    long_description='Python wrapper for controlling an OLED display',
    ext_modules=[module1]
)
