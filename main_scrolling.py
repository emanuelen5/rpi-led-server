from oled.scrolling_text import ScrollingLines, ScrollingLine, ScrollType
from adafruit_pypixelbuf import wheel
import cv2
import numpy as np

if __name__ == "__main__":
    buffer = np.zeros((64, 300, 3), dtype=np.float32)
    s = ScrollingLines([
        ScrollingLine(f"{s.name}....................", s) for s in ScrollType
    ] + [ScrollingLine("SHORT TEXT")])
    split_line = 128
    while True:
        buffer[:, :, :] = 0
        buffer[:, split_line+1, :] = (1, 1, 1)
        buffer[:, :split_line] = s.render(buffer[:, :split_line])
        for i, line in enumerate(s.lines):
            state_color = wheel(line._state.value / len(line._state.__class__) * 255)
            line.font.put_string(buffer, split_line+2, i * line.font.height, f"{line._state.value}: {line._state.name}", fg=state_color)
        img = cv2.resize(buffer, dsize=None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
        cv2.imshow("SCROLLING_LINE", img)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
