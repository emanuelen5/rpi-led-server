from dataclasses import dataclass, field
from unittest.mock import patch, MagicMock
import cv2
import numpy as np
import math
import time
import logging

logger = logging.getLogger(__name__)


@dataclass
class RotatyEncoderHW_Model:
    PIN_CLK: int
    PIN_BTN: int
    PIN_DT: int
    steps: int = 15
    pressed: bool = False
    pressed_time: float = field(repr=False, init=False, default=0)
    timeout: float = 0.1

    def __post_init__(self):
        self._pin_callbacks = {self.PIN_DT: [], self.PIN_CLK: [], self.PIN_BTN: []}
        self._pin_values = {self.PIN_DT: False, self.PIN_CLK: True, self.PIN_BTN: False}
        self.rotation = 0
        self.GPIO_mock = MagicMock()
        self.GPIO_mock.add_event_detect.side_effect = self.register_cb
        self._patcher = patch("rpi.GPIO", new=MagicMock)
        self._patcher.start()
        self.rotation_per_step = 2 * math.pi / self.steps

    def register_cb(self, pin, direction, callback, *args, **kwargs):
        if pin in self._pin_callbacks:
            self._pin_callbacks[pin].append(callback)
        else:
            logger.warning("Callback for unrelated pin will not be registered")

    def press(self):
        self.pressed = True
        self.pressed_time = time.time()
        self._toggle_pin(self.PIN_BTN)

    def _toggle_pin(self, pin):
        self._pin_values[pin] = not self._pin_values[pin]
        for cb in self._pin_callbacks[pin]:
            cb(pin)

    def rotate(self, clockwise: bool):
        self.rotation += 1 if clockwise else -1
        if clockwise:
            self._toggle_pin(self.PIN_DT)
        self._toggle_pin(self.PIN_CLK)
        if not clockwise:
            self._toggle_pin(self.PIN_DT)
        self._toggle_pin(self.PIN_CLK)

    def refresh(self):
        disp = np.zeros((200, 200, 3), dtype=np.uint8)
        radius = 40 if self.pressed else 50
        if self.pressed and time.time() - self.pressed_time > self.timeout:
            self.pressed = False
            self._toggle_pin(self.PIN_BTN)
        rotation = self.rotation * self.rotation_per_step
        pt2 = np.array([100, 100]) + np.array([math.sin(rotation), -math.cos(rotation)]) * radius
        cv2.line(disp, (100, 100), tuple(pt2.astype(np.int16)), (123, 50, 168), thickness=3, lineType=cv2.LINE_AA)
        cv2.circle(disp, (100, 100), radius, (255, 255, 255), thickness=5, lineType=cv2.LINE_AA)

        cv2.putText(disp, "CLK: " + str(self._pin_values[self.PIN_CLK]), (5, 20), cv2.FONT_HERSHEY_PLAIN, 1,
                    (255, 255, 255), thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(disp, "DT: " + str(self._pin_values[self.PIN_DT]), (5, 40), cv2.FONT_HERSHEY_PLAIN, 1,
                    (255, 255, 255), thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(disp, "BTN: " + str(self._pin_values[self.PIN_BTN]), (5, 60), cv2.FONT_HERSHEY_PLAIN, 1,
                    (255, 255, 255), thickness=1, lineType=cv2.LINE_AA)
        cv2.imshow("rotary_encoder_hw", disp)


RIGHT_ARROW = 65363
LEFT_ARROW = 65361
UP_ARROW = 65362
DOWN_ARROW = 65364


def main():
    rot = RotatyEncoderHW_Model(1, 2, 3)
    k = None
    while k != ord("q"):
        k = cv2.waitKeyEx(1)
        if k == LEFT_ARROW:
            rot.rotate(False)
        elif k == RIGHT_ARROW:
            rot.rotate(True)
        elif k == DOWN_ARROW:
            rot.press()
        rot.refresh()


if __name__ == "__main__":
    main()
