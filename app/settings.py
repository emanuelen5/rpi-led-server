import logging
import pickle
import time
from leds import NeoPixel
from rotary_encoder import RotaryEncoder
from oled.display import Display
from dataclasses import dataclass
from enum import Enum, auto
from oled.scrolling_text import ScrollingLines, ScrollingLine

logger = logging.getLogger(__name__)


class LED_Mode(Enum):
    COLOR = auto()
    RAINBOW = auto()


class MainMode(Enum):
    DEMO = auto()
    BLANK = auto()
    NOTIFICATIONS = auto()
    STATUS = auto()


class SelectMode(Enum):
    MAIN_WINDOW = auto()
    LED_BRIGHTNESS = auto()
    LED_COLOR = auto()
    LED_EFFECT = auto()
    EFFECT_SPEED = auto()
    EFFECT_STRENGTH = auto()


@dataclass
class LED_Settings:
    brightness: float = 1.0
    color_index: int = 0
    cycle_index: int = 0
    speed: float = 0
    strength: float = 1.0


class Globals:
    led_mode = LED_Mode.COLOR
    main_mode = MainMode.DEMO
    select_mode = SelectMode.MAIN_WINDOW
    led_settings: LED_Settings = LED_Settings()
    show_viewer: bool = False
    running: bool = True
    last_interaction: float = time.time()
    screen_saver_time: float = 600
    oled_model: Display
    led_model: NeoPixel
    rotenc_model: RotaryEncoder
    header_line = ScrollingLine("SEL: ")
    value_line = ScrollingLine("=")
    status_lines = ScrollingLines([
        ScrollingLine(),
        ScrollingLine()
    ], 24)
    notifications = [ScrollingLine("1: Homeassistant")]
    SESSION_FILE = ".led-server.session"

    @classmethod
    def save(cls, filename: str = None):
        if filename is None:
            filename = cls.SESSION_FILE
        logger.info(f"Saving current session to {filename}")
        with open(filename, "wb") as f:
            pickle.dump({k: getattr(cls, k) for k in (
                "led_mode", "main_mode", "select_mode",
                "led_settings", "screen_saver_time")
                         }, f)

    @classmethod
    def load(cls, filename: str = None):
        if filename is None:
            filename = cls.SESSION_FILE
        logger.info(f"Restoring previous session from {filename}")
        with open(filename, "rb") as f:
            v = pickle.load(f)
            for k, v in v.items():
                setattr(cls, k, v)
