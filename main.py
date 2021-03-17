from oled import OLED
from oled.fonts import put_string, Font1206
from datetime import datetime
from enum import Enum, auto
from leds import create_pixels
from leds.color import wheel
from argparse import ArgumentParser
from rotary_encoder import RotaryEncoder
from threading import Thread
from util import KeyCode
from dataclasses import dataclass
import time
import cv2
import numpy as np

parser = ArgumentParser()
parser.add_argument("--pixel-count", "-p", type=int, default=50, help="The number of pixels")
args = parser.parse_args()

# The number of NeoPixels
num_pixels = args.pixel_count

pixels = create_pixels(num_pixels=50)


class LED_Mode(Enum):
    COLOR = auto()
    RAINBOW = auto()


class SelectMode(Enum):
    TIME = auto()
    LED_BRIGHTNESS = auto()
    LED_COLOR = auto()
    LED_EFFECT = auto()
    EFFECT_SPEED = auto()


@dataclass
class LED_Settings:
    brightness: float = 1.0
    color_index: int = 0
    cycle_index: int = 0
    speed: float = 0


def cycle_enum(enum_value: Enum, forwards: bool = True):
    cls = enum_value.__class__
    enums = list(cls)
    idx = enums.index(enum_value)
    if forwards:
        idx_new = (idx + 1) % len(cls)
    else:
        idx_new = (idx - 1) % len(cls)
    try:
        return enums[idx_new]
    except:
        print(f"Enums: {enums}")
        print(f"idx_new: {idx_new}")


class Globals:
    led_mode = LED_Mode.COLOR
    select_mode = SelectMode.TIME
    led_settings: LED_Settings = LED_Settings()
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
            put_string(display.buffer, 5, 0,  f"LED: {Globals.led_mode.name}", fg=(1., 1., 1.), font=Font1206)
            put_string(display.buffer, 5, 10, f"SEL: {Globals.select_mode.name}", fg=(1., 1., 1.), font=Font1206)
            put_string(display.buffer, 0, 36, dt.strftime("%H:%M:%S.%f"), fg=(1., 0., 1.), bg=(1., 1., 1.), alpha=0.3)
            put_string(display.buffer, 0, 26, dt.strftime("%Y-%m-%d"), fg=(1., 0., 0.), bg=None, alpha=1)
            put_string(display.buffer, 0, 46, "Emaus demo", bg=(1., 1., 0.), fg=None, alpha=0.7)
            Globals.buffer_oled = display.refresh()


def pixels_update_buffer():
    Globals.buffer_leds = original_show()


original_show = pixels.show
pixels.show = pixels_update_buffer


def main_leds():
    pixels.fill((0, 0, 0))
    pixels.show()
    while Globals.running:
        if Globals.led_mode == LED_Mode.COLOR:
            pixels.fill((np.array(list(wheel(Globals.led_settings.color_index))) * Globals.led_settings.brightness).astype(
                np.uint8))
            pixels.show()
        elif Globals.led_mode == LED_Mode.RAINBOW:
            for i in range(num_pixels):
                pixel_index = (i * 255 // num_pixels) + Globals.led_settings.cycle_index
                pixels[i] = (np.array(list(wheel(int(pixel_index) & 255))) * Globals.led_settings.brightness).astype(np.uint8)
            pixels.show()
            Globals.led_settings.cycle_index += Globals.led_settings.speed
        time.sleep(0.001)


def on_rotate(cw: bool):
    if Globals.select_mode == SelectMode.LED_BRIGHTNESS:
        diff = Globals.led_settings.brightness * 0.05 + 0.001
        diff = diff if cw else -diff
        Globals.led_settings.brightness = max(0, min(Globals.led_settings.brightness + diff, 1.0))
    elif Globals.select_mode == SelectMode.LED_COLOR:
        diff = 1 if cw else -1
        Globals.led_settings.color_index = (Globals.led_settings.color_index + diff) % 256
    elif Globals.select_mode == SelectMode.EFFECT_SPEED:
        diff = Globals.led_settings.speed * 0.1
        diff = diff if cw else -diff
        Globals.led_settings.speed = max(0.001, min(Globals.led_settings.speed + diff, 1.0))
    elif Globals.select_mode == SelectMode.LED_EFFECT:
        Globals.led_mode = cycle_enum(Globals.led_mode, cw)


def on_press(down: bool):
    if down:
        Globals.select_mode = cycle_enum(Globals.select_mode)


def main_rotenc():
    rotenc = RotaryEncoder()
    rotenc.register_rotation_callback(on_rotate)
    rotenc.register_press_callback(on_press)
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


t1 = Thread(target=main_leds, daemon=True)
t2 = Thread(target=main_display, daemon=True)
t3 = Thread(target=main_rotenc, daemon=True)
threads = (t1, t2, t3)
for t in threads:
    t.start()


print("Press q to exit")
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
    cv2.imshow("LEDS", Globals.buffer_leds)
