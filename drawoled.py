from oled import OLED
from datetime import datetime
from oled.fonts import put_string


def main():
    with OLED() as display:
        while True:
            display.clear()
            dt = datetime.now()
            put_string(display.buffer, 0, 16, dt.strftime("%Y-%m-%d"), fg=(1., 0., 0.))
            put_string(display.buffer, 0, 26, dt.strftime("%H:%M:%S.%f"), fg=(1., 0., 1.))
            put_string(display.buffer, 0, 46, "Emaus demo", fg=(1., 1., 0.))
            display.display()


if __name__ == "__main__":
    main()
