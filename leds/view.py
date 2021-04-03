import cv2
import numpy as np
from typing import Tuple
from dataclasses import dataclass
from .model import LED_BaseModel


@dataclass
class LED_ModelView:
    pixels: LED_BaseModel
    brightness: float = 1.0
    scale: Tuple[int, int] = (6, 6)

    def render(self) -> np.ndarray:
        frame_buffer = cv2.resize(
            self.pixels.buffer.reshape((1, len(self.pixels), 3)), dsize=None,
            fx=self.scale[1], fy=self.scale[0], interpolation=cv2.INTER_NEAREST)
        return self.brightness / 255.0 * frame_buffer
