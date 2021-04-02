import logging
from rotary_encoder import RotaryEncoder
from rotary_encoder.rotary_encoder import RotaryEncoderView
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--no-viewer", action="store_true", help="Do not open an X-window that shows the display's currently shown image")
args = parser.parse_args()
show_viewer = not args.no_viewer

if show_viewer:
    import cv2


def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    enc = RotaryEncoder()

    if show_viewer:
        view = RotaryEncoderView(enc)

    while True:
        if show_viewer:
            cv2.imshow("ROTARY_ENCODER", view.render())


if __name__ == "__main__":
    main()
