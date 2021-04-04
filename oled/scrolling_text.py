from enum import Enum, auto
from typing import List
from dataclasses import dataclass, field
import time
from .fonts import Font, Font1206
import numpy as np


class ScrollType(Enum):
    ROLLING = auto()
    REVERSING = auto()


class LineState(Enum):
    INIT = auto()
    SCROLLING = auto()
    SCROLLING_ROLLOVER = auto()
    SCROLLING_BACK = auto()
    END = auto()


@dataclass
class ScrollingLine:
    string: str = ""
    scroll_type: ScrollType = ScrollType.ROLLING
    line_time: float = 5.0
    font: Font = Font1206
    _state: LineState = LineState.INIT
    _start_time: float = field(init=False, repr=False, compare=False, default_factory=time.time)
    _offset: int = field(init=False, default=0)

    def service(self):
        now = time.time()
        state_time = now - self._start_time
        if self._state == LineState.INIT:
            if state_time > self.line_time/5:
                self.set_state(LineState.SCROLLING)
        elif self._state == LineState.SCROLLING:
            if state_time > self.line_time/5:
                self.set_state(LineState.END)
        elif self._state == LineState.END:
            if state_time > self.line_time/5:
                if self.scroll_type == ScrollType.ROLLING:
                    self.set_state(LineState.SCROLLING_ROLLOVER)
                elif self.scroll_type == ScrollType.REVERSING:
                    self.set_state(LineState.SCROLLING_BACK)
        elif self._state in (LineState.SCROLLING_ROLLOVER, LineState.SCROLLING_BACK):
            if state_time > self.line_time/5:
                self.set_state(LineState.INIT)

    def set_state(self, state: LineState):
        self._start_time = time.time()
        self._state = state

    def render(self, img: np.ndarray, offset_y: int = 0) -> np.ndarray:
        if self._state == LineState.INIT:
            self.font.put_string(img, 0, offset_y, self.string)
        elif self._state == LineState.SCROLLING:
            self.font.put_string(img, -30, offset_y, self.string)
        elif self._state == LineState.END:
            self.font.put_string(img, -50, offset_y, self.string)
        elif self._state == LineState.SCROLLING_ROLLOVER:
            self.font.put_string(img, -50, offset_y, self.string)
        elif self._state == LineState.SCROLLING_BACK:
            self.font.put_string(img, -50, offset_y, self.string)
        return img


@dataclass
class ScrollingLines:
    lines: List[ScrollingLine] = field(default_factory=list)

    def service(self):
        for line in self.lines:
            line.service()

    def render(self, img: np.ndarray) -> np.ndarray:
        offset_y = 0
        for line in self.lines:
            line.render(img, offset_y)
            offset_y += line.font.height
        return img


