from rpi import GPIO
from time import sleep
from enum import IntEnum
from dataclasses import dataclass, field
from typing import List, Callable
from logging import getLogger, basicConfig, INFO

logger = getLogger(__name__)
basicConfig(format='%(levelname)s:%(message)s', level=INFO)


class PINS(IntEnum):
    CLK = 5
    DT = 6
    BTN = 13


@dataclass
class RotaryEncoder:
    counter: int = field(default=0, compare=False)
    last_clk_state: bool = None
    cb_rotation: List[Callable[[bool], None]] = field(default_factory=lambda: [], init=False, repr=False, compare=False)
    cb_press: List[Callable[[], None]] = field(default_factory=lambda: [], init=False, repr=False, compare=False)

    def __post_init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PINS.CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(PINS.DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(PINS.BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.last_clk_state = GPIO.input(PINS.CLK)

        GPIO.add_event_detect(PINS.CLK, GPIO.BOTH, callback=self.rotation_callback, bouncetime=5)
        GPIO.add_event_detect(PINS.BTN, GPIO.BOTH, callback=self.button_callback, bouncetime=5)

    def register_rotation_callback(self, cb: Callable[[bool], None]):
        self.cb_rotation.append(cb)

    def register_press_callback(self, cb: Callable[[], None]):
        self.cb_press.append(cb)

    def rotation_callback(self, channel: int):
        pin = PINS(channel)
        value = GPIO.input(pin)

        if value:
            logger.debug(f"{pin} - rising")
        else:
            logger.debug(f"{pin} - falling")

        clk_state = GPIO.input(PINS.CLK)
        dt_state = GPIO.input(PINS.DT)
        if clk_state != self.last_clk_state:
            was_clockwise = dt_state != clk_state
            if was_clockwise:
                self.counter += 1
            else:
                self.counter -= 1
            logger.info(f"Counter: {self.counter}")

            for cb in self.cb_rotation:
                cb(was_clockwise)
        self.last_clk_state = clk_state

    def button_callback(self, channel: int):
        pin = PINS(channel)
        value = GPIO.input(pin)

        if value:
            logger.debug(f"{pin} - rising")
        else:
            logger.debug(f"{pin} - falling")

        for cb in self.cb_press:
            cb()


def main():
    rot_enc = RotaryEncoder()

    try:
        while True:
            sleep(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
