from oled import OLED
from oled.display.display import DisplayModelViewer
from oled.fonts import put_string
from oled.scrolling_text import ScrollingLine, ScrollingLines
from datetime import datetime
from enum import Enum, auto
from leds import create_pixels
from leds.view import LED_ModelView
from leds.color import wheel
from argparse import ArgumentParser
from rotary_encoder import RotaryEncoder
from rotary_encoder.rotary_encoder import RotaryEncoderView
from threading import Thread
import queue
from functools import partial
import logging
import pickle
import signal
import subprocess
import sys
from util import KeyCode
import util
from dataclasses import dataclass
import time
import cv2
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = ArgumentParser()
parser.add_argument("--pixel-count", "-p", type=int, default=50, help="The number of pixels")
parser.add_argument("--no-viewer", action="store_true", help="Do not open a viewer with a render of the model state")
parser.add_argument("--new-session", action="store_true",
                    help="Do not try to load settings from previous session at start")
parser.add_argument("--demo", action="store_true", help="Automatically step through modes")
args = parser.parse_args()

# The number of NeoPixels
num_pixels = args.pixel_count

pixels = create_pixels(num_pixels=num_pixels)


class LED_Mode(Enum):
    COLOR = auto()
    RAINBOW = auto()


class MainMode(Enum):
    DEMO = auto()
    BLANK = auto()
    NOTIFICATIONS = auto()
    STATUS = auto()


class SelectMode(Enum):
    MAIN_WINDOW = auto()
    LED_BRIGHTNESS = auto()
    LED_COLOR = auto()
    LED_EFFECT = auto()
    EFFECT_SPEED = auto()
    EFFECT_STRENGTH = auto()


@dataclass
class LED_Settings:
    brightness: float = 1.0
    color_index: int = 0
    cycle_index: int = 0
    speed: float = 0
    strength: float = 1.0


def cycle_enum(enum_value: Enum, forwards: bool = True):
    cls = enum_value.__class__
    enums = list(cls)
    idx = enums.index(enum_value)
    if forwards:
        idx_new = (idx + 1) % len(cls)
    else:
        idx_new = (idx - 1) % len(cls)
    return enums[idx_new]


class Globals:
    led_mode = LED_Mode.COLOR
    main_mode = MainMode.DEMO
    select_mode = SelectMode.MAIN_WINDOW
    led_settings: LED_Settings = LED_Settings()
    show_viewer: bool = not args.no_viewer
    running: bool = True
    last_interaction: float = time.time()
    screen_saver_time: float = 600
    buffer_oled: np.ndarray = np.empty((1, 1, 1))
    buffer_leds: np.ndarray = np.empty((1, 1, 1))
    buffer_rotenc: np.ndarray = np.empty((1, 1, 1))
    keypress_rotenc = queue.Queue()
    header_line = ScrollingLine("SEL: ")
    value_line = ScrollingLine("=")
    status_lines = ScrollingLines([
        ScrollingLine(),
        ScrollingLine()
    ], 24)
    notifications = [ScrollingLine("1: Homeassistant")]
    SESSION_FILE = ".led-server.session"

    @classmethod
    def save(cls, filename: str = None):
        if filename is None:
            filename = cls.SESSION_FILE
        logger.info(f"Saving current session to {filename}")
        with open(filename, "wb") as f:
            pickle.dump({k: getattr(cls, k) for k in (
                "led_mode", "main_mode", "select_mode",
                "led_settings", "show_viewer", "screen_saver_time")
            }, f)

    @classmethod
    def load(cls, filename: str = None):
        if filename is None:
            filename = cls.SESSION_FILE
        logger.info(f"Restoring previous session from {filename}")
        with open(filename, "rb") as f:
            v = pickle.load(f)
            for k, v in v.items():
                setattr(cls, k, v)


if not args.new_session:
    try:
        Globals.load()
    except FileNotFoundError:
        logger.info("No previous led session file found")


def main_display():
    with OLED() as display:
        view = DisplayModelViewer(display)
        while Globals.running:
            display.clear()
            if time.time() - Globals.last_interaction > Globals.screen_saver_time:
                display.refresh()
                time.sleep(0.2)
                continue
            Globals.header_line.string = f"SEL: {Globals.select_mode.name}"
            Globals.header_line.render(display.buffer, 0, fg=(1., 1., 1.), bg=None)
            if Globals.select_mode == SelectMode.LED_EFFECT:
                value_line = f"={Globals.led_mode.name}"
            elif Globals.select_mode == SelectMode.EFFECT_SPEED:
                value_line = f"={Globals.led_settings.speed:5.4f}"
            elif Globals.select_mode == SelectMode.EFFECT_STRENGTH:
                value_line = f"={Globals.led_settings.strength:5.4f}"
            elif Globals.select_mode == SelectMode.LED_BRIGHTNESS:
                value_line = f"={Globals.led_settings.brightness:5.3f}"
            elif Globals.select_mode == SelectMode.LED_COLOR:
                value_line = f"={Globals.led_settings.color_index:3d}"
            elif Globals.select_mode == SelectMode.MAIN_WINDOW:
                value_line = f"={Globals.main_mode.name}"
            Globals.value_line.string = value_line
            Globals.value_line.render(display.buffer, 12, fg=(1., 1., 1.), bg=None)
            if Globals.main_mode == MainMode.DEMO:
                dt = datetime.now()
                put_string(display.buffer, 0, 36, dt.strftime("%H:%M:%S.%f"), fg=(1., 0., 1.), bg=(1., 1., 1.), alpha=0.3)
                put_string(display.buffer, 0, 26, dt.strftime("%Y-%m-%d"), fg=(0., 0., 1.), bg=None, alpha=1)
                put_string(display.buffer, 0, 46, "Emaus demo", bg=(0., 1., 1.), fg=None, alpha=0.7)
            elif Globals.main_mode == MainMode.BLANK:
                pass
            elif Globals.main_mode == MainMode.NOTIFICATIONS:
                if len(Globals.notifications) == 0:
                    put_string(display.buffer, 0, 26, "No notifications", fg=(0., 1., 0.))
                else:
                    for i, notification in enumerate(Globals.notifications):
                        notification.render(display.buffer, 26 + i * 12, bg=None)
            elif Globals.main_mode == MainMode.STATUS:
                Globals.status_lines.lines[0].string = f"IP:{', '.join(util.get_ips())}"
                Globals.status_lines.lines[1].string = util.get_uptime()
                Globals.status_lines.render(display.buffer)
            if len(Globals.notifications):
                put_string(display.buffer, 90, 52, f"{len(Globals.notifications):1d}", fg=(0., 0., 1.), bg=None)
            if Globals.show_viewer:
                Globals.buffer_oled = view.render()
            else:
                display.refresh()


def main_leds():
    pixels.fill((0, 0, 0))
    pixels.show()
    view = LED_ModelView(pixels, scale=(200, 20))
    last_time = time.time()
    while Globals.running:
        current_time = time.time()
        time_since_last = current_time - last_time
        last_time = current_time
        if Globals.led_mode == LED_Mode.COLOR:
            pixels.fill((np.array(list(wheel(Globals.led_settings.color_index))) * Globals.led_settings.brightness).astype(
                np.uint8))
        elif Globals.led_mode == LED_Mode.RAINBOW:
            c_effect_strength = 255 / num_pixels * Globals.led_settings.strength
            for i in range(num_pixels):
                pixel_index = (i * c_effect_strength) + Globals.led_settings.cycle_index + Globals.led_settings.color_index
                pixels[i] = (np.array(list(wheel(int(pixel_index) & 0xff))) * Globals.led_settings.brightness).astype(np.uint8)
            Globals.led_settings.cycle_index += Globals.led_settings.speed * time_since_last * 512
        pixels.show()
        if Globals.show_viewer:
            Globals.buffer_leds = view.render()


def on_rotate(cw: bool):
    Globals.last_interaction = time.time()
    if Globals.select_mode == SelectMode.LED_BRIGHTNESS:
        diff = Globals.led_settings.brightness * 0.05 + 0.001
        diff = diff if cw else -diff
        Globals.led_settings.brightness = max(0, min(Globals.led_settings.brightness + diff, 1.0))
    elif Globals.select_mode == SelectMode.LED_COLOR:
        diff = 1 if cw else -1
        Globals.led_settings.color_index = (Globals.led_settings.color_index + diff) % 256
    elif Globals.select_mode == SelectMode.EFFECT_STRENGTH:
        diff = Globals.led_settings.strength * 0.01 + 0.01
        diff = diff if cw else -diff
        Globals.led_settings.strength = max(0.001, min(Globals.led_settings.strength + diff, 1.0))
    elif Globals.select_mode == SelectMode.EFFECT_SPEED:
        diff = Globals.led_settings.speed * 0.01 + 0.01
        diff = diff if cw else -diff
        Globals.led_settings.speed = max(0.001, min(Globals.led_settings.speed + diff, 1.0))
    elif Globals.select_mode == SelectMode.LED_EFFECT:
        Globals.led_mode = cycle_enum(Globals.led_mode, cw)
    elif Globals.select_mode == SelectMode.MAIN_WINDOW:
        Globals.main_mode = cycle_enum(Globals.main_mode, cw)


def on_press(down: bool):
    Globals.last_interaction = time.time()
    if down:
        Globals.select_mode = cycle_enum(Globals.select_mode)


def main_rotenc():
    rotenc = RotaryEncoder()
    rotenc.register_rotation_callback(on_rotate)
    rotenc.register_press_callback(on_press)

    if not Globals.show_viewer:
        return

    view = RotaryEncoderView(rotenc)
    while Globals.running:
        try:
            k = Globals.keypress_rotenc.get_nowait()
        except queue.Empty:
            k = -1
        if k in (KeyCode.LEFT_ARROW, ord('h')):
            rotenc.rotate(False)
        elif k in (KeyCode.RIGHT_ARROW, ord('l')):
            rotenc.rotate(True)
        elif k in (KeyCode.DOWN_ARROW, ord('j')):
            view.press_temp()
        elif k in (KeyCode.UP_ARROW, ord('k')):
            view.press_toggle()
        Globals.buffer_rotenc = view.render()


def demo():
    shell_cmd = partial(subprocess.run, encoding="utf-8", shell=True, capture_output=True)

    def keypress(_winid: int, keys: str, sleep_time: int = 0.03, count: int = 1):
        p = shell_cmd("xdotool getactivewindow")
        active_winid = int(p.stdout.strip())
        if (not Globals.running) or active_winid != _winid:
            print("Exiting demo thread")
            sys.exit(0)
        repeat_str = f" x{count}" if count > 1 else ""
        print(f"Sending key strokes: {keys}{repeat_str}")
        for _ in range(count):
            shell_cmd(f"xdotool key --window 0 --clearmodifiers {keys}")
            time.sleep(sleep_time)
        time.sleep(1.0)

    for _ in range(50):
        p = shell_cmd("xdotool search --name 'ROTARY_ENCODER'")
        try:
            winid = int(p.stdout.strip())
            break
        except ValueError:
            pass
        time.sleep(0.1)
    else:
        raise RuntimeError("Could not find the OpenCV window")
    shell_cmd(f"xdotool windowactivate {winid}")
    keypress = partial(keypress, winid)

    time.sleep(0.5)

    while True:
        keypress("l", sleep_time=1.0, count=3)

        # Brightness
        keypress("j")
        keypress("h", count=30)
        keypress("l", count=40)

        # Phase
        keypress("j")
        keypress("h", count=30)
        keypress("l", count=30)

        # LED effect
        keypress("j")
        keypress("l")

        # LED effect speed
        keypress("j")
        keypress("l", count=30)

        # LED effect strength
        keypress("j")
        keypress("h", count=30)

        # Back to main menu
        keypress("j")


def stop_nice(_signal, _frametype):
    Globals.running = False
    Globals.save()
    sys.exit(0)


signal.signal(signal.SIGTERM, stop_nice)


t1 = Thread(target=main_leds, daemon=True)
t2 = Thread(target=main_display, daemon=True)
t3 = Thread(target=main_rotenc, daemon=True)
threads = [t1, t2, t3]
for t in threads:
    t.start()

if Globals.show_viewer:
    WINDOW_LEDS = "LEDS"
    WINDOW_ROTENC = "ROTARY_ENCODER"
    WINDOW_OLED = "OLED_DISPLAY"

    cv2.namedWindow(WINDOW_LEDS)
    cv2.namedWindow(WINDOW_ROTENC)
    cv2.namedWindow(WINDOW_OLED)

    time.sleep(0.5)  # Fix for making sure moveWindow actually bites
    cv2.moveWindow(WINDOW_LEDS, 200, 650)
    cv2.moveWindow(WINDOW_ROTENC, 780, 370)
    cv2.moveWindow(WINDOW_OLED, 200, 200)

    if args.demo:
        t = Thread(target=demo, daemon=True)
        t.start()
        threads.append(t)

    print("Press q to exit")
    while Globals.running:
        k = cv2.waitKeyEx(1)
        if k == ord('q'):
            Globals.running = False
            Globals.save()
            break
        else:
            Globals.keypress_rotenc.put(k)
        cv2.imshow(WINDOW_LEDS, Globals.buffer_leds)
        cv2.imshow(WINDOW_ROTENC, Globals.buffer_rotenc)
        cv2.imshow(WINDOW_OLED, Globals.buffer_oled)

else:
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass

Globals.running = False
for t in threads:
    t.join()
