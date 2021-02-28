import unittest
import liboled
import numpy as np


class TestSmoke(unittest.TestCase):
    def test_has_take_array(self):
        self.assertTrue(hasattr(liboled, "take_array"))

    def test_take_array(self):
        arr = np.zeros((50,50,3))
        self.assertTrue(liboled.take_array(arr))

    def test_take_array_badcall(self):
        arr = np.zeros((50,50,3))
        self.assertTrue(liboled.take_array(arr, arr))


if __name__ == '__main__':
    unittest.main()
