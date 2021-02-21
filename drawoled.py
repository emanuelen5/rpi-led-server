import oled
import ssd1331
import numpy as np
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Display:
    buffer: np.ndarray = field(default_factory=lambda: np.zeros((64, 32, 3), dtype=np.float32))

    def clear(self):
        pass

    def string(self, x, y, s: str, color=(1., 1., 1.)):
        pass

    def display(self):
        pass


class OLED:
    def __enter__(self) -> Display:
        self.open()
        d = Display()
        return d

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @staticmethod
    def open():
        if not ssd1331.init():
            raise OSError("Could not initialize the BCM module")
        ssd1331.begin()
        ssd1331.clear()

    @staticmethod
    def close():
        ssd1331.spi_end()
        ssd1331.close()


def main():
    with OLED as o:
        o.clear()
        o.string(0, 16, datetime.now().strftime("%Y-%m-%d %H:%M"), color=(1., 0., 0.))
        o.string(6, 46, "Emaus demo", color=(1., 1., 0.))
        o.display()


if __name__ == "__main__":
    main()
