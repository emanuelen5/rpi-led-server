import unittest

from rotary_encoder import RotaryEncoder, PINS


class TestSmoke(unittest.TestCase):
    def setUp(self) -> None:
        self.object = RotaryEncoder()

    def test_pass(self):
        pass


if __name__ == '__main__':
    unittest.main()

