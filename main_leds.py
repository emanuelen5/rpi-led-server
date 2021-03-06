import time
from argparse import ArgumentParser
from leds import create_pixels
from leds.view import LED_ModelView
from leds.color import rainbow_cycle
import sys
import cv2

parser = ArgumentParser()
parser.add_argument("--pixel-count", "-p", type=int, default=50, help="The number of pixels")
parser.add_argument(
    "--no-viewer",
    action="store_true",
    help="Do not open an X-window that shows the display's currently shown image")
args = parser.parse_args()
show_viewer = not args.no_viewer

# The number of NeoPixels
num_pixels = args.pixel_count

pixels = create_pixels(num_pixels=50, brightness=1.0)
if show_viewer:
    view = LED_ModelView(pixels, scale=(200, 20))
    original_show = pixels.show

    def show_interactive():
        original_show()
        cv2.imshow("LEDS", view.render())
        k = cv2.waitKeyEx(1)
        if k == ord('q'):
            sys.exit(0)
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

    rainbow_cycle(pixels, 0.001, 5)  # rainbow cycle with 1ms delay per step
