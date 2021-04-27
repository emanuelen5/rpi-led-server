from oled import OLED
from datetime import datetime
from app.settings import Globals, SelectMode, MainMode, LED_Mode
from leds import create_pixels
from leds.color import wheel
from rotary_encoder import RotaryEncoder
from threading import Thread
from util import cycle_enum
import time
import numpy as np
from oled.fonts import put_string
from .util import get_ips, get_uptime

threads = []


def main_display():
    with OLED() as display:
        Globals.oled_model = display
        while Globals.running:
            display.clear()
            if time.time() - Globals.last_interaction > Globals.screen_saver_time:
                display.refresh()
                time.sleep(0.2)
                continue
            Globals.header_line.string = f"SEL: {Globals.select_mode.name}"
            Globals.header_line.render(display.back_buffer, 0, fg=(1., 1., 1.), bg=None)
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
            Globals.value_line.render(display.back_buffer, 12, fg=(1., 1., 1.), bg=None)
            if Globals.main_mode == MainMode.DEMO:
                dt = datetime.now()
                put_string(display.back_buffer, 0, 36, dt.strftime("%H:%M:%S.%f"), fg=(1., 0., 1.), bg=(1., 1., 1.), alpha=0.3)
                put_string(display.back_buffer, 0, 26, dt.strftime("%Y-%m-%d"), fg=(0., 0., 1.), bg=None, alpha=1)
                put_string(display.back_buffer, 0, 46, "Emaus demo", bg=(0., 1., 1.), fg=None, alpha=0.7)
            elif Globals.main_mode == MainMode.BLANK:
                pass
            elif Globals.main_mode == MainMode.NOTIFICATIONS:
                if len(Globals.notifications) == 0:
                    put_string(display.back_buffer, 0, 26, "No notifications", fg=(0., 1., 0.))
                else:
                    for i, notification in enumerate(Globals.notifications):
                        notification.render(display.back_buffer, 26 + i * 12, bg=None)
            elif Globals.main_mode == MainMode.STATUS:
                Globals.status_lines.lines[0].string = f"IP:{', '.join(get_ips())}"
                Globals.status_lines.lines[1].string = get_uptime()
                Globals.status_lines.render(display.back_buffer)
            if len(Globals.notifications):
                put_string(display.back_buffer, 90, 52, f"{len(Globals.notifications):1d}", fg=(0., 0., 1.), bg=None)
            display.refresh()


def main_leds(num_pixels: int):
    pixels = create_pixels(num_pixels=num_pixels)
    Globals.led_model = pixels
    pixels.fill((0, 0, 0))
    pixels.show()
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
    Globals.rotenc_model = rotenc
    rotenc.register_rotation_callback(on_rotate)
    rotenc.register_press_callback(on_press)


def start(num_pixels: int):
    t1 = Thread(target=main_leds, args=(num_pixels, ), daemon=True)
    t2 = Thread(target=main_display, daemon=True)
    t3 = Thread(target=main_rotenc, daemon=True)
    threads.extend([t1, t2, t3])
    for t in threads:
        t.start()


def stop():
    Globals.running = False
    for t in threads:
        t.join()
