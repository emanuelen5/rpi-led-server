from oled.display.display import DisplayModelViewer
from app.settings import Globals
from leds.view import LED_ModelView
from argparse import ArgumentParser
from rotary_encoder.rotary_encoder import RotaryEncoderView
from threading import Thread
from functools import partial
import logging
import signal
import subprocess
import sys
from util import KeyCode
import time
import cv2
import app.app as app


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
Globals.show_viewer = not args.no_viewer


if not args.new_session:
    try:
        Globals.load()
    except FileNotFoundError:
        logger.info("No previous led session file found")


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
    app.stop()
    sys.exit(0)


signal.signal(signal.SIGTERM, stop_nice)
app.start(num_pixels)


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

    oled_view = DisplayModelViewer(Globals.oled_model)
    led_view = LED_ModelView(Globals.led_model, scale=(200, 20))
    rotenc_view = RotaryEncoderView(Globals.rotenc_model)

    if args.demo:
        t = Thread(target=demo, daemon=True)
        t.start()
        app.threads.append(t)

    print("Press q to exit")
    while Globals.running:
        k = cv2.waitKeyEx(1)
        if k == ord('q'):
            Globals.running = False
            Globals.save()
            break
        elif k in (KeyCode.LEFT_ARROW, ord('h')):
            Globals.rotenc_model.rotate(False)
        elif k in (KeyCode.RIGHT_ARROW, ord('l')):
            Globals.rotenc_model.rotate(True)
        elif k in (KeyCode.DOWN_ARROW, ord('j')):
            rotenc_view.press_temp()
        elif k in (KeyCode.UP_ARROW, ord('k')):
            rotenc_view.press_toggle()

        cv2.imshow(WINDOW_LEDS, led_view.render())
        cv2.imshow(WINDOW_ROTENC, rotenc_view.render())
        cv2.imshow(WINDOW_OLED, oled_view.render())

else:
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass


app.stop()
