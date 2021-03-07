from oled import OLED
from datetime import datetime


def main():
    with OLED() as display:
        while True:
            display.clear()
            dt = datetime.now()
            display.string(0, 16, dt.strftime("%Y-%m-%d"), color=(1., 0., 0.))
            display.string(0, 26, dt.strftime("%H:%M:%S.%f"), color=(1., 0., 1.))
            display.string(0, 46, "Emaus demo", color=(1., 1., 0.))
            display.display()


if __name__ == "__main__":
    main()
