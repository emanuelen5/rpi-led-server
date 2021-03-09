from oled import OLED
from datetime import datetime
from oled.fonts import put_string


def main():
    with OLED() as display:
        while True:
            display.clear()
            dt = datetime.now()
            put_string(display.buffer, 0, 26, dt.strftime("%H:%M:%S.%f"), fg=(1., 0., 1.), bg=(1., 1., 1.), alpha=0.3)
            put_string(display.buffer, 0, 16, dt.strftime("%Y-%m-%d"), fg=(1., 0., 0.), bg=None, alpha=1)
            put_string(display.buffer, 0, 36, "Emaus demo", bg=(1., 1., 0.), fg=None, alpha=0.7)
            display.display()


if __name__ == "__main__":
    main()
