import unittest
import liboled


class TestSmoke(unittest.TestCase):
    def test_asd(self):
        self.assertIsNotNone(liboled.asd)


if __name__ == '__main__':
    unittest.main()
