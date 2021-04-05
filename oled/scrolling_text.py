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
    SCROLLING_ROLLOVER = auto()
    SCROLLING_BACK = auto()
    END = auto()


@dataclass
class ScrollingLine:
    _string: str = ""
    scroll_type: ScrollType = ScrollType.SCROLL_RESET
    speed: float = 20.0
    pause_time: float = 3.0
    font: Font = Font1206
    _state: LineState = LineState.INIT
    _start_time: float = field(init=False, repr=False, compare=False, default_factory=time.time)
    _offset: int = field(init=False, default=0)

    @property
    def string(self):
        return self._string

    @string.setter
    def string(self, v):
        if len(self.string) != len(v):
            self.set_state(LineState.INIT)
        self._string = v

    def set_state(self, state: LineState):
        self._start_time = time.time()
        self._state = state

    def render(self, img: np.ndarray, offset_y: int = 0, **kwargs) -> np.ndarray:
        width = img.shape[1]
        now = time.time()
        state_time = now - self._start_time
        line_length = self.font.width * len(self.string)
        end_offset = width - line_length
        if self._state == LineState.INIT:
            self._offset = 0
            if line_length <= width:
                self.set_state(LineState.INIT)
            elif state_time > self.pause_time:
                self.set_state(LineState.SCROLLING_OVER)
        elif self._state == LineState.SCROLLING_OVER:
            self._offset = max(end_offset, -int(self.speed * state_time))
            if self._offset <= end_offset:
                self.set_state(LineState.END)
        elif self._state == LineState.END:
            self._offset = end_offset
            if state_time > self.pause_time / 2:
                if self.scroll_type == ScrollType.ROLLING:
                    self.set_state(LineState.SCROLLING_ROLLOVER)
                elif self.scroll_type == ScrollType.REVERSING:
                    self.set_state(LineState.SCROLLING_BACK)
                elif self.scroll_type == ScrollType.SCROLL_RESET:
                    self.set_state(LineState.INIT)
        elif self._state == LineState.SCROLLING_ROLLOVER:
            next_offset = -line_length - self.font.width
            self._offset = max(next_offset, end_offset-int(self.speed * state_time))
            self.font.put_string(img, self._offset + line_length + self.font.width, offset_y, self.string, **kwargs)
            if self._offset <= next_offset:
                self.set_state(LineState.INIT)
        elif self._state == LineState.SCROLLING_BACK:
            self._offset = min(0, int(self.speed * state_time) + end_offset)
            if self._offset >= 0:
                self.set_state(LineState.INIT)
        self.font.put_string(img, self._offset, offset_y, self.string, **kwargs)
        return img


@dataclass
class ScrollingLines:
    lines: List[ScrollingLine] = field(default_factory=list)

    def render(self, img: np.ndarray) -> np.ndarray:
        offset_y = 0
        for line in self.lines:
            line.render(img, offset_y)
            offset_y += line.font.height
        return img


