from rpi import GPIO
from util import KeyCode
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
    cb_rotation: List[Callable[[bool], None]] = field(default_factory=lambda: [], init=False, repr=False, compare=False)
    cb_press: List[Callable[[], None]] = field(default_factory=lambda: [], init=False, repr=False, compare=False)

    def register_rotation_callback(self, cb: Callable[[bool], None]):
        self.cb_rotation.append(cb)

    def register_press_callback(self, cb: Callable[[], None]):
        self.cb_press.append(cb)


@dataclass
class RotaryEncoder(RotaryEncoderBase):
    counter: int = field(default=0, compare=False)
    dt_state: bool = None
    cb_rotation: List[Callable[[bool], None]] = field(default_factory=lambda: [], init=False, repr=False, compare=False)
    cb_press: List[Callable[[], None]] = field(default_factory=lambda: [], init=False, repr=False, compare=False)

    def __post_init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PINS.CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(PINS.DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(PINS.BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.dt_state = GPIO.input(PINS.DT)

        GPIO.add_event_detect(PINS.CLK, GPIO.BOTH, callback=self.rotation_callback, bouncetime=5)
        GPIO.add_event_detect(PINS.BTN, GPIO.BOTH, callback=self.button_callback, bouncetime=5)

    def rotation_callback(self, channel: int):
        pin = PINS(channel)
        pin_value = GPIO.input(pin)

        if pin_value:
            logger.debug(f"{pin} - rising")
        else:
            logger.debug(f"{pin} - falling")

        if pin is PINS.CLK:
            was_clockwise = self.dt_state != pin_value
            if was_clockwise:
                self.counter += 1
            else:
                self.counter -= 1
            logger.info(f"Counter: {self.counter}")

            for cb in self.cb_rotation:
                cb(was_clockwise)
        elif pin is PINS.DT:
            self.dt_state = pin_value

    def button_callback(self, channel: int):
        pin = PINS(channel)
        value = GPIO.input(pin)

        if value:
            logger.debug(f"{pin} - rising")
        else:
            logger.debug(f"{pin} - falling")

            for cb in self.cb_press:
                cb()

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
class RotaryEncoderMock(RotaryEncoderBase):
    steps: int = 15
    pressed: bool = False
    pressed_time: float = field(repr=False, init=False, default=0)
    timeout: float = 0.1

    def __post_init__(self):
        self.rotation = 0
        self.rotation_per_step = 2 * math.pi / self.steps
        self._timeout = self.timeout

    def press(self):
        self.pressed = True
        self.pressed_time = time.time()
        self._timeout = self.timeout

    def press_toggle(self):
        self.pressed = not self.pressed
        self._timeout = float("inf")

    def rotate(self, clockwise: bool):
        self.rotation += 1 if clockwise else -1

    def refresh(self):
        disp = np.zeros((200, 200, 3), dtype=np.uint8)
        radius = 40 if self.pressed else 50
        if self.pressed and time.time() - self.pressed_time > self._timeout:
            self.pressed = False
        rotation = self.rotation * self.rotation_per_step
        pt2 = np.array([100, 100]) + np.array([math.sin(rotation), -math.cos(rotation)]) * radius
        cv2.line(disp, (100, 100), tuple(pt2.astype(np.int16)), (123, 50, 168), thickness=3, lineType=cv2.LINE_AA)
        cv2.circle(disp, (100, 100), radius, (255, 255, 255), thickness=5, lineType=cv2.LINE_AA)
        cv2.imshow("rotary_encoder_mock", disp)

    @classmethod
    def main(cls):
        rot = cls()
        print(f"Use the arrow keys: {list(KeyCode)} to rotate and press the rotary encoder.")
        k = None
        while k != ord("q"):
            k = cv2.waitKeyEx(1)
            if k == KeyCode.LEFT_ARROW:
                rot.rotate(False)
            elif k == KeyCode.RIGHT_ARROW:
                rot.rotate(True)
            elif k == KeyCode.DOWN_ARROW:
                rot.press()
            elif k == KeyCode.UP_ARROW:
                rot.press_toggle()
            rot.refresh()
