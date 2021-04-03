import logging
from rotary_encoder import RotaryEncoder
from rotary_encoder.rotary_encoder import RotaryEncoderView
from util import KeyCode
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--no-viewer", action="store_true", help="Do not open an X-window that shows the display's currently shown image")
args = parser.parse_args()
show_viewer = not args.no_viewer

if show_viewer:
    import cv2


def main_viewer():
    enc = RotaryEncoder()
    view = RotaryEncoderView(enc)

    while True:
        print(f"Use the arrow keys: {list(KeyCode)} to rotate and press the rotary encoder.")
        while True:
            k = cv2.waitKeyEx(1)
            if k == ord('q'):
                return
            elif k in (KeyCode.LEFT_ARROW, ord('h')):
                view.rotary_encoder.rotate(False)
            elif k in (KeyCode.RIGHT_ARROW, ord('l')):
                view.rotary_encoder.rotate(True)
            elif k in (KeyCode.DOWN_ARROW, ord('j')):
                view.press_temp()
            elif k in (KeyCode.UP_ARROW, ord('k')):
                view.press_toggle()
            cv2.imshow("ROTARY_ENCODER", view.render())


def main_no_viewer():
    RotaryEncoder.main()


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    if show_viewer:
        main_viewer()
    else:
        main_no_viewer()
