import time
from argparse import ArgumentParser
from leds import create_pixels
from leds.mock import LED_ModelView
import sys
import cv2

parser = ArgumentParser()
parser.add_argument("--pixel-count", "-p", type=int, default=50, help="The number of pixels")
args = parser.parse_args()

# The number of NeoPixels
num_pixels = args.pixel_count

pixels = create_pixels(num_pixels=50)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return r, g, b


def rainbow_cycle(wait, duration=1.0):
    start_time = time.time()
    while time.time() - start_time < duration:
        for j in range(255):
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels) + j
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            time.sleep(wait)


k = None
if isinstance(pixels, LED_ModelView):
    show_orig = pixels.show

    def show_interactive():
        r = show_orig()
        k = cv2.waitKeyEx(1)
        if k == ord('q'):
            sys.exit(0)
        return r
    pixels.show = show_interactive

while True:
    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(1)

    rainbow_cycle(0.001, 5)  # rainbow cycle with 1ms delay per step
