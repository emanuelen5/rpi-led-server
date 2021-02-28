import unittest
import liboled
import numpy as np


class TestSmoke(unittest.TestCase):
    def setUp(self) -> None:
        self.arr = np.random.random((liboled.OLED_HEIGHT, liboled.OLED_WIDTH, 3))

    def tearDown(self) -> None:
        liboled.deinit()

    def test_has_take_array(self):
        self.assertTrue(hasattr(liboled, "take_array"))

    def test_init_array_only_once(self):
        liboled.init(self.arr)
        with self.assertRaises(Exception):
            liboled.init(self.arr)

    def test_init_then_deinit(self):
        liboled.init(self.arr)
        liboled.deinit()

    def test_take_array_passes_by_reference(self):
        arr = self.arr
        res = liboled.take_array(arr)
        arr[0, 0] = arr[0, 0] - 1
        self.assertTrue((res == arr).all())

    def test_take_array_badcall(self):
        arr = self.arr
        with self.assertRaises(TypeError):
            self.assertTrue(liboled.take_array(arr, arr))
        with self.assertRaises(TypeError):
            self.assertTrue(liboled.take_array(arr, test=arr))


if __name__ == '__main__':
    unittest.main()
