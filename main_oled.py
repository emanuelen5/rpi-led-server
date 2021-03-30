from oled import OLED
from oled.display.display import DisplayModelView
from datetime import datetime
from oled.fonts import put_string
from liboled import OLED_WIDTH, OLED_HEIGHT
import cv2
import numpy as np
import time


def main():
    with OLED() as display:
        display_view = DisplayModelView(display)
        image_smol1 = cv2.cvtColor(cv2.resize(cv2.imread("test-image.png"), dsize=(OLED_WIDTH, OLED_HEIGHT), interpolation=cv2.INTER_AREA).astype(np.float32) / 256., cv2.COLOR_BGR2RGB)
        image_smol2 = cv2.cvtColor(cv2.resize(cv2.imread("test-image2.png"), dsize=(OLED_WIDTH, OLED_HEIGHT), interpolation=cv2.INTER_AREA).astype(np.float32) / 256., cv2.COLOR_BGR2RGB)
        start_time = time.time()
        print("Press q to exit")
        while True:
            k = cv2.waitKeyEx(1)
            if k == ord("q"):
                break
            display.clear()
            idx = (time.time() - start_time) // 10 % 3
            if idx == 0:
                display.buffer = image_smol1.copy()
            elif idx == 1:
                display.buffer = image_smol2.copy()
            elif idx == 2:
                dt = datetime.now()
                put_string(display.buffer, 0, 26, dt.strftime("%H:%M:%S.%f"), fg=(1., 0., 1.), bg=(1., 1., 1.), alpha=0.3)
                put_string(display.buffer, 0, 16, dt.strftime("%Y-%m-%d"), fg=(1., 0., 0.), bg=None, alpha=1)
                put_string(display.buffer, 0, 36, "Emaus demo", bg=(1., 1., 0.), fg=None, alpha=0.7)

            display.refresh()
            cv2.imshow("OLED", display_view.render())


if __name__ == "__main__":
    main()
