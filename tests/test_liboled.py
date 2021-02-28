import unittest
import liboled
import numpy as np


class TestSmoke(unittest.TestCase):
    def test_has_take_array(self):
        self.assertTrue(hasattr(liboled, "take_array"))

    def test_take_array_passes_by_reference(self):
        arr = np.random.random((50, 50, 3))
        res = liboled.take_array(arr)
        arr[0, 0] = arr[0, 0] - 1
        self.assertTrue((res == arr).all())

    def test_take_array_badcall(self):
        arr = np.zeros((50, 50, 3))
        with self.assertRaises(TypeError):
            self.assertTrue(liboled.take_array(arr, arr))


if __name__ == '__main__':
    unittest.main()
