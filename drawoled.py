from oled import OLED
from datetime import datetime
import time


def main():
    with OLED() as display:
        while True:
            display.clear()
            dt = datetime.now()
            display.string(0, 0, dt.strftime("%Y-%m-%d"), color=(1., 0., 0.))
            display.string(0, 16, dt.strftime("%H:%M:%S.%f"), color=(1., 0., 0.))
            display.string(0, 36, "Emaus demo", color=(1., 1., 0.))
            display.display()
            print(dt)
            time.sleep(0.5)


if __name__ == "__main__":
    main()
