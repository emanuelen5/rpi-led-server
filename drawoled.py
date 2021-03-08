from oled import OLED
from datetime import datetime
from oled.fonts import put_string
import time
import atexit
import numpy as np

render_times = []


def print_mean_time():
    print("Render times:")
    print(f" - samples: {len(render_times)}")

    if len(render_times) == 0:
        return

    print(f" -    mean: {np.mean(render_times) * 1000:6.4f} ms")
    print(f" -     min: {np.min(render_times) * 1000:6.4f} ms")
    print(f" -     std: {np.std(render_times) * 1000:6.4f} ms")
    print(f" -   (max): {np.max(render_times) * 1000:6.4f} ms")


atexit.register(print_mean_time)


def main():
    with OLED() as display:
        while True:
            display.clear()
            dt = datetime.now()
            start_time = time.time()
            put_string(display.buffer, 0, 16, dt.strftime("%Y-%m-%d"), fg=(1., 0., 0.))
            put_string(display.buffer, 0, 26, dt.strftime("%H:%M:%S.%f"), fg=(1., 0., 1.))
            put_string(display.buffer, 0, 46, "Emaus demo", fg=(1., 1., 0.))
            render_times.append(time.time() - start_time)
            display.display()
            if len(render_times) >= 100:
                break


if __name__ == "__main__":
    main()
