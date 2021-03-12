from dataclasses import dataclass
from unittest.mock import patch, MagicMock
import cv2
import numpy as np
import math


@dataclass
class RotatyEncoderHW_Model:
    PIN_CLK: int
    PIN_BTN: int
    PIN_DT: int
    steps: int = 15

    def __post_init__(self):
        self._clk_event = []
        self._btn_event = []
        self._dt_event = []
        self.rotation = 0
        self.GPIO_mock = MagicMock()
        self.GPIO_mock.add_event_detect.side_effect = self.register_cb
        self._patcher = patch("rpi.GPIO", new=MagicMock)
        self._patcher.start()
        self.rotation_per_step = 2 * math.pi / self.steps

    def register_cb(self, pin, direction, callback, *args, **kwargs):
        if pin == self.PIN_CLK:
            self._clk_event.append(callback)
        elif pin == self.PIN_BTN:
            self._btn_event.append(callback)
        elif pin == self.PIN_DT:
            self._dt_event.append(callback)

    def rotate(self, clockwise: bool):
        self.rotation += 1 if clockwise else -1
        for cb in self._clk_event:
            cb(self.PIN_CLK)

    def refresh(self):
        disp = np.zeros((200, 200, 3), dtype=np.float32)
        rotation = self.rotation * self.rotation_per_step
        pt2 = np.array([100, 100]) + np.array([math.sin(rotation), -math.cos(rotation)]) * 50
        cv2.line(disp, (100, 100), tuple(pt2.astype(np.int16)), (123, 50, 168), thickness=3, lineType=cv2.LINE_AA)
        cv2.circle(disp, (100, 100), 50, (255, 255, 255), thickness=5, lineType=cv2.LINE_AA)
        cv2.imshow("rotary_encoder_hw", disp)


def main():
    rot = RotatyEncoderHW_Model(1, 2, 3)
    rot.refresh()
    while (k := cv2.waitKeyEx(1)) != ord("q"):
        if k == ord("h"):
            rot.rotate(False)
            rot.refresh()
        elif k == ord("l"):
            rot.rotate(True)
            rot.refresh()
        elif k != -1:
            print(k)


if __name__ == "__main__":
    main()
