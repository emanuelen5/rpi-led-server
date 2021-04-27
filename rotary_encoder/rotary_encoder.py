from rpi import GPIO
from time import sleep
from enum import IntEnum
from dataclasses import dataclass, field
from typing import List, Callable
import logging
import cv2
import numpy as np
import math
import time

logger = logging.getLogger(__name__)


class PINS(IntEnum):
    CLK = 5
    DT = 6
    BTN = 13


@dataclass
class RotaryEncoderBase:
    rotation: int = field(default=0, compare=False)
    pressed: bool = False
    cb_rotation: List[Callable[[bool], None]] = field(default_factory=lambda: [], init=False, repr=False, compare=False)
    cb_press: List[Callable[[bool], None]] = field(default_factory=lambda: [], init=False, repr=False, compare=False)

    def register_rotation_callback(self, cb: Callable[[bool], None]):
        self.cb_rotation.append(cb)

    def rotate(self, cw: bool):
        self.rotation += 1 if cw else -1
        logger.debug(f"Rotation: {self.rotation}")
        for cb in self.cb_rotation:
            cb(cw)

    def register_press_callback(self, cb: Callable[[], None]):
        self.cb_press.append(cb)

    def press(self, pressed_down: bool):
        self.pressed = pressed_down
        for cb in self.cb_press:
            cb(pressed_down)


@dataclass
class RotaryEncoderGPIOModel(RotaryEncoderBase):
    _dt_state: bool = None

    def __post_init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PINS.CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(PINS.DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(PINS.BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self._dt_state = GPIO.input(PINS.DT)
        self.pressed = GPIO.input(PINS.BTN)

        GPIO.add_event_detect(PINS.CLK, GPIO.BOTH, callback=self.gpio_clk_pin_callback, bouncetime=5)
        GPIO.add_event_detect(PINS.BTN, GPIO.BOTH, callback=self.gpio_btn_pin_callback, bouncetime=5)

    def gpio_clk_pin_callback(self, channel: int):
        pin_value = GPIO.input(PINS.CLK)
        dt_pin_value = GPIO.input(PINS.DT)

        if pin_value:
            logger.debug("CLK rising")
        else:
            logger.debug("CLK falling")

        was_clockwise = dt_pin_value != pin_value
        self.rotate(was_clockwise)

    def gpio_btn_pin_callback(self, channel: int):
        pin = PINS(channel)
        value = GPIO.input(pin)

        if value:
            logger.debug(f"{pin} - rising")
        else:
            logger.debug(f"{pin} - falling")
        self.press(value)

    @classmethod
    def main(cls):
        _ = cls()
        try:
            while True:
                sleep(0.01)
        except KeyboardInterrupt:
            pass
        finally:
            GPIO.cleanup()


@dataclass
class RotaryEncoderView:
    rotary_encoder: RotaryEncoderBase
    steps: int = 15
    pressed_time: float = field(repr=False, init=False, default=0)
    timeout: float = 0.1

    def __post_init__(self):
        # Make sure that timeouts are cleared if the button overrides
        def clear_timeout(*args, **kwargs):
            self._timeout = None
        self.rotary_encoder.register_press_callback(clear_timeout)
        self.rotation = 0
        self.rotation_per_step = 2 * math.pi / self.steps
        self._timeout = None

    def _press(self, timeout):
        self.pressed_time = time.time()
        self.rotary_encoder.press(not self.rotary_encoder.pressed)
        self._timeout = timeout

    def press_temp(self, timeout=None):
        if timeout is None:
            timeout = self.timeout
        self._press(timeout)

    def press_toggle(self):
        self._press(None)

    def render(self) -> np.ndarray:
        disp = np.zeros((200, 200, 3), dtype=np.uint8)
        radius = 40 if self.rotary_encoder.pressed else 50
        if self._timeout and time.time() - self.pressed_time > self._timeout:
            self.press_toggle()
        rotation = self.rotary_encoder.rotation * self.rotation_per_step
        pt2 = np.array([100, 100]) + np.array([math.sin(rotation), -math.cos(rotation)]) * radius
        cv2.line(disp, (100, 100), tuple(pt2.astype(np.int16)), (123, 50, 168), thickness=3, lineType=cv2.LINE_AA)
        cv2.circle(disp, (100, 100), radius, (255, 255, 255), thickness=5, lineType=cv2.LINE_AA)
        return disp
