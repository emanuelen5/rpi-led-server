import numpy as np
import cv2
from dataclasses import dataclass, field
import liboled


@dataclass
class DisplayModel:
    front_buffer: np.ndarray = field(
        default_factory=lambda: np.zeros((liboled.OLED_HEIGHT, liboled.OLED_WIDTH, 3), dtype=np.float32))
    back_buffer: np.ndarray = field(
        default_factory=lambda: np.zeros((liboled.OLED_HEIGHT, liboled.OLED_WIDTH, 3), dtype=np.float32))

    def clear(self):
        self.back_buffer[:, :, :] = 0.0

    def string(self, x, y, s: str, color=(1., 1., 1.)):
        cv2.putText(self.back_buffer, s, (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.25, color)

    def refresh(self):
        """
        Copies the back-buffer into the front-buffer (shows it on the display)
        """
        self.front_buffer[:, :, :] = self.back_buffer[:, :, :]
        self.front_buffer[self.front_buffer < 0] = 0
        self.front_buffer[self.front_buffer > 1.0] = 1.0
        liboled.display(self.front_buffer)

    def get_buffer(self) -> np.ndarray:
        front_buffer_from_display = liboled.get_buffer().astype(np.float32)
        front_buffer_from_display = cv2.cvtColor(front_buffer_from_display, cv2.COLOR_RGB2BGR)
        front_buffer_from_display[:, :, 0] = front_buffer_from_display[:, :, 0] * 1.0 / 0xF8
        front_buffer_from_display[:, :, 1] = front_buffer_from_display[:, :, 1] * 1.0 / 0xFC
        front_buffer_from_display[:, :, 2] = front_buffer_from_display[:, :, 2] * 1.0 / 0xF8
        return front_buffer_from_display

    def open(self):
        liboled.init()

    @staticmethod
    def close():
        liboled.deinit()


@dataclass
class DisplayModelViewer:
    """
    Renders a bitmap representation of the Display Model.
    """
    model: DisplayModel
    scaling: float = 6.0
    rendered_buffer: np.ndarray = field(init=False, default=None, repr=False)

    def __post_init__(self):
        # Pre-compute grid
        scaled_buffer = cv2.resize(self.model.back_buffer, fx=self.scaling, fy=self.scaling, dsize=None)
        y, x, z = scaled_buffer.shape
        X, Y, _ = np.meshgrid(range(x), range(y), range(z))
        self.grid = (Y % self.scaling == self.scaling - 1) | (X % self.scaling == self.scaling - 1)

    def render(self) -> np.ndarray:
        buffer = self.model.front_buffer.copy()
        buffer = cv2.resize(buffer, fx=self.scaling, fy=self.scaling, dsize=None, interpolation=cv2.INTER_NEAREST)
        # Make grid
        buffer[self.grid] = 0.1 + buffer[self.grid] * 0.9
        # Make border
        buffer = cv2.copyMakeBorder(buffer, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=(1., 1., 1.))
        self.rendered_buffer = buffer
        return buffer
