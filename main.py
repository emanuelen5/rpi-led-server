from oled import OLED
from oled.fonts import put_string
from datetime import datetime
from enum import Enum, auto
from leds import create_pixels
from leds.color import rainbow_cycle
from argparse import ArgumentParser
from rotary_encoder import RotaryEncoder
from threading import Thread
from util import KeyCode
import time
import cv2
import numpy as np

parser = ArgumentParser()
parser.add_argument("--pixel-count", "-p", type=int, default=50, help="The number of pixels")
args = parser.parse_args()

# The number of NeoPixels
num_pixels = args.pixel_count

pixels = create_pixels(num_pixels=50)


class Modes(Enum):
    IDLE = auto()


class Globals:
    mode = Modes.IDLE
    running: bool = True
    buffer_oled: np.ndarray = np.empty((1, 1, 1))
    buffer_leds: np.ndarray = np.empty((1, 1, 1))
    buffer_rotenc: np.ndarray = np.empty((1, 1, 1))
    keypress_rotenc = []
    keypress_oled = []
    keypress_leds = []


def main_display():
    with OLED() as display:
        while Globals.running:
            display.clear()
            dt = datetime.now()
            put_string(display.buffer, 0, 26, dt.strftime("%H:%M:%S.%f"), fg=(1., 0., 1.), bg=(1., 1., 1.), alpha=0.3)
            put_string(display.buffer, 0, 16, dt.strftime("%Y-%m-%d"), fg=(1., 0., 0.), bg=None, alpha=1)
            put_string(display.buffer, 0, 36, "Emaus demo", bg=(1., 1., 0.), fg=None, alpha=0.7)
            Globals.buffer_oled = display.refresh()


def main_leds():
    while Globals.running:
        pixels.fill((255, 0, 0))
        pixels.show()
        time.sleep(1)

        pixels.fill((0, 255, 0))
        pixels.show()
        time.sleep(1)

        pixels.fill((0, 0, 255))
        pixels.show()
        time.sleep(1)

        rainbow_cycle(pixels, 0.001, 5)  # rainbow cycle with 1ms delay per step


def main_rotenc():
    rotenc = RotaryEncoder()
    while Globals.running:
        k = Globals.keypress_rotenc.pop() if len(Globals.keypress_rotenc) else -1
        if k in (KeyCode.LEFT_ARROW, ord('h')):
            rotenc.rotate(False)
        elif k in (KeyCode.RIGHT_ARROW, ord('l')):
            rotenc.rotate(True)
        elif k in (KeyCode.DOWN_ARROW, ord('j')):
            rotenc.press()
        elif k in (KeyCode.UP_ARROW, ord('k')):
            rotenc.press_toggle()
        Globals.buffer_rotenc = rotenc.render()


print("Press q to exit")

t1 = Thread(target=main_leds, daemon=True)
t2 = Thread(target=main_display, daemon=True)
t3 = Thread(target=main_rotenc, daemon=True)
threads = (t1, t2, t3)
for t in (t2, t3):
    t.start()

while True:
    k = cv2.waitKeyEx(1)
    if k == ord('q'):
        Globals.running = False
        break
    else:
        Globals.keypress_rotenc.append(k)
        Globals.keypress_oled.append(k)
        Globals.keypress_leds.append(k)
    cv2.imshow("OLED_DISPLAY", Globals.buffer_oled)
    cv2.imshow("ROTARY_ENCODER", Globals.buffer_rotenc)



