from oled import OLED
from datetime import datetime


def main():
    with OLED() as display:
        while True:
            display.clear()
            display.string(0, 16, datetime.now().strftime("%Y-%m-%d %H:%M"), color=(1., 0., 0.))
            display.string(6, 46, "Emaus demo", color=(1., 1., 0.))
            display.display()


if __name__ == "__main__":
    main()
