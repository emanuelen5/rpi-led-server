import logging
from rotary_encoder import RotaryEncoder


def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    RotaryEncoder().main()


if __name__ == "__main__":
    main()
