from dataclasses import dataclass, field
from .display import Display


@dataclass
class OLED:
    display: Display = field(default=None, init=False)

    def __enter__(self) -> Display:
        self.display = Display()
        self.display.open()
        return self.display

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.display.close()
