import unittest
import liboled
import numpy as np
import numpy.testing


class TestSmoke(unittest.TestCase):
    def setUp(self) -> None:
        self.arr = np.random.random((liboled.OLED_HEIGHT, liboled.OLED_WIDTH, 3))

    def tearDown(self) -> None:
        try:
            liboled.deinit()
        except RuntimeError:
            pass

    def test_has_functions(self):
        self.assertTrue(hasattr(liboled, "take_array"))
        self.assertTrue(hasattr(liboled, "get_array"))
        self.assertTrue(hasattr(liboled, "init"))
        self.assertTrue(hasattr(liboled, "deinit"))
        self.assertTrue(hasattr(liboled, "display"))

    def test_error_on_double_init(self):
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


class TestLibOled(unittest.TestCase):
    def setUp(self) -> None:
        self.arr = np.random.random((liboled.OLED_HEIGHT, liboled.OLED_WIDTH, 3))
        liboled.init(self.arr)

    def tearDown(self) -> None:
        try:
            liboled.deinit()
        except RuntimeError:
            pass

    def test_display(self):
        liboled.display()

    def test_get_array(self):
        arr = liboled.get_array()
        numpy.testing.assert_equal(self.arr, arr)


if __name__ == '__main__':
    unittest.main()
