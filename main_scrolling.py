from oled.scrolling_text import ScrollingLines, ScrollingLine, ScrollType
import cv2
import numpy as np

if __name__ == "__main__":
    buffer = np.zeros((96, 64, 3), dtype=np.float32)
    s = ScrollingLines([
        ScrollingLine("IP: 255.255.255.0", ScrollType.ROLLING),
        ScrollingLine("IP: 255.255.255.0", ScrollType.ROLLING)]
    )
    while True:
        buffer[:, :, :] = 0
        s.service()
        buffer = s.render(buffer)
        cv2.imshow("SCROLLING_LINE", buffer)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
