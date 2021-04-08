from oled.scrolling_text import ScrollingLines, ScrollingLine, ScrollType
from adafruit_pypixelbuf import wheel
from typing import Tuple
from enum import Enum
import cv2
import numpy as np

buffer = np.zeros((64, 300, 3), dtype=np.float32)
s = ScrollingLines(
    [ScrollingLine(f"{s.name}....................", s) for s in ScrollType]
    + [ScrollingLine("SHORT TEXT")])


def state_to_color(state: Enum) -> Tuple[int, int, int]:
    return wheel(state.value / len(state.__class__) * 255)


if __name__ == "__main__":
    split_line = 128
    while True:
        buffer[:, :, :] = 0
        buffer[:, split_line + 1, :] = (1, 1, 1)
        buffer[:, :split_line] = s.render(buffer[:, :split_line])
        for i, line in enumerate(s.lines):
            line.font.put_string(
                buffer, split_line + 2, i * line.font.height,
                f"{line._state.value}: {line._state.name}", fg=state_to_color(line._state))
        img = cv2.resize(buffer, dsize=None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
        cv2.imshow("SCROLLING_LINE", img)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
