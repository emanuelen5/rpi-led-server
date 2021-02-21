import unittest
import oled


class TestSmoke(unittest.TestCase):
    def test_asd(self):
        self.assertIsNotNone(oled.asd)


if __name__ == '__main__':
    unittest.main()
