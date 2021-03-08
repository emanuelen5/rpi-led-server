from RPi import GPIO
from time import sleep
from enum import IntEnum
from dataclasses import dataclass
from logging import getLogger, basicConfig, INFO

logger = getLogger(__name__)
basicConfig(format='%(levelname)s:%(message)s', level=INFO)


class PINS(IntEnum):
    CLK = 5
    DT = 6
    BTN = 13


GPIO.setmode(GPIO.BCM)
GPIO.setup(PINS.CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PINS.DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PINS.BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


@dataclass
class RotaryEncoder:
    counter: int = 0

    def __post_init__(self):
        self.last_clk_state = self.clk_state = GPIO.input(PINS.CLK)
        self.dt_state = GPIO.input(PINS.DT)

        GPIO.add_event_detect(PINS.CLK, GPIO.BOTH, callback=self.rotation_callback, bouncetime=5)
        GPIO.add_event_detect(PINS.BTN, GPIO.BOTH, callback=self.button_callback, bouncetime=5)

    def rotation_callback(self, channel: int):
        pin = PINS(channel)
        value = GPIO.input(pin)

        if value:
            logger.debug(f"{pin} - rising")
        else:
            logger.debug(f"{pin} - falling")

        self.clk_state = GPIO.input(PINS.CLK)
        self.dt_state = GPIO.input(PINS.DT)
        if self.clk_state != self.last_clk_state:
            if self.dt_state != self.clk_state:
                self.counter += 1
            else:
                self.counter -= 1
            logger.info(f"Counter: {self.counter}")
        self.last_clk_state = self.clk_state

    def button_callback(self, channel: int):
        pin = PINS(channel)
        value = GPIO.input(pin)

        if value:
            logger.debug(f"{pin} - rising")
        else:
            logger.debug(f"{pin} - falling")


rot_enc = RotaryEncoder()

try:
    while True:
        sleep(0.01)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
