from enum import Enum, auto
from typing import List
from dataclasses import dataclass, field
import time
from .fonts import Font, Font1206
import numpy as np


class ScrollType(Enum):
    SCROLL_RESET = auto()
    ROLLING = auto()
    REVERSING = auto()


class LineState(Enum):
    INIT = auto()
    SCROLLING_OVER = auto()
    SCROLLING_TO_END = auto()
    SCROLLING_ROLLOVER = auto()
    SCROLLING_BACK = auto()
    END = auto()


@dataclass
class ScrollingLine:
    string: str = ""
    scroll_type: ScrollType = ScrollType.ROLLING
    speed: float = 20.0
    pause_time: float = 1.0
    font: Font = Font1206
    _state: LineState = LineState.INIT
    _start_time: float = field(init=False, repr=False, compare=False, default_factory=time.time)
    _offset: int = field(init=False, default=0)

    def service(self):
        now = time.time()
        state_time = now - self._start_time
        if self._state == LineState.INIT:
            if state_time > self.pause_time:
                self.set_state(LineState.SCROLLING_OVER)
        elif self._state == LineState.SCROLLING_OVER:
            line_Length = self.font.width * len(self.string)
            if self._offset <= -line_Length:
                self.set_state(LineState.END)
        elif self._state == LineState.SCROLLING_TO_END:
            line_Length = self.font.width * len(self.string)
            if self._offset <= -line_Length:
                self.set_state(LineState.END)
        elif self._state == LineState.END:
            if state_time > self.pause_time:
                if self.scroll_type == ScrollType.ROLLING:
                    self.set_state(LineState.SCROLLING_ROLLOVER)
                elif self.scroll_type == ScrollType.REVERSING:
                    self.set_state(LineState.SCROLLING_BACK)
        elif self._state in (LineState.SCROLLING_ROLLOVER, LineState.SCROLLING_BACK):
            if state_time > self.pause_time:
                self.set_state(LineState.INIT)

    def set_state(self, state: LineState):
        self._start_time = time.time()
        self._state = state

    def render(self, img: np.ndarray, offset_y: int = 0) -> np.ndarray:
        now = time.time()
        state_time = now - self._start_time
        line_Length = self.font.width * len(self.string)
        if self._state == LineState.INIT:
            self._offset = 0
        elif self._state == LineState.SCROLLING_OVER:
            self._offset = max(-line_Length, -int(self.speed * state_time))
        elif self._state == LineState.SCROLLING_TO_END:
            self._offset = max(-line_Length, -int(self.speed * state_time))
        elif self._state == LineState.END:
            self._offset = 0
        elif self._state == LineState.SCROLLING_ROLLOVER:
            self._offset = 0
        elif self._state == LineState.SCROLLING_BACK:
            self._offset = 0
        self.font.put_string(img, self._offset, offset_y, self.string)
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


