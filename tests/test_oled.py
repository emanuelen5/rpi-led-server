import unittest
from oled import OLED


class TestSmoke(unittest.TestCase):
    def test_context(self):
        with OLED() as display:
            display.clear()
            display.string(0, 0, "TEST string", (1, 1, 1))


if __name__ == '__main__':
    unittest.main()
