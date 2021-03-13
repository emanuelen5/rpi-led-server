from oled import OLED
from datetime import datetime
from oled.fonts import put_string
import cv2


def main():
    with OLED() as display:
        print("Press q to exit")
        k = None
        while k != ord("q"):
            display.clear()
            dt = datetime.now()
            put_string(display.buffer, 0, 26, dt.strftime("%H:%M:%S.%f"), fg=(1., 0., 1.), bg=(1., 1., 1.), alpha=0.3)
            put_string(display.buffer, 0, 16, dt.strftime("%Y-%m-%d"), fg=(1., 0., 0.), bg=None, alpha=1)
            put_string(display.buffer, 0, 36, "Emaus demo", bg=(1., 1., 0.), fg=None, alpha=0.7)
            display.refresh()
            k = cv2.waitKeyEx(1)


if __name__ == "__main__":
    main()
