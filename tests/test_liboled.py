import unittest
import liboled
import numpy as np
import numpy.testing
from parameterized import parameterized


def custom_name_func_shape(testcase_func, param_num, param):
    return f"{testcase_func.__name__}-{'x'.join(str(x) for x in param.args[0])}"


def custom_name_func(testcase_func, param_num, param):
    return f"{testcase_func.__name__}{parameterized.to_safe_name('_'.join(str(x) for x in param.args))}"


class TestSmoke(unittest.TestCase):
    def setUp(self) -> None:
        self.arr = np.random.random((liboled.OLED_HEIGHT, liboled.OLED_WIDTH, 3))

    def tearDown(self) -> None:
        try:
            liboled.deinit()
        except RuntimeError:
            pass

    def test_has_functions(self):
        self.assertTrue(hasattr(liboled, "get_array"))
        self.assertTrue(hasattr(liboled, "init"))
        self.assertTrue(hasattr(liboled, "deinit"))
        self.assertTrue(hasattr(liboled, "display"))
        self.assertTrue(hasattr(liboled, "get_buffer"))

    def test_error_on_double_init(self):
        liboled.init(self.arr)
        with self.assertRaises(Exception):
            liboled.init(self.arr)

    def test_init_then_deinit(self):
        liboled.init(self.arr)
        liboled.deinit()

    def test_init_passes_by_reference(self):
        arr = self.arr
        liboled.init(arr)
        res = liboled.get_array()
        arr[0, 0] = arr[0, 0] - 1
        numpy.testing.assert_equal(arr, res)

    def test_can_take_float(self):
        arr = np.random.random((liboled.OLED_HEIGHT, liboled.OLED_WIDTH, 3)).astype(dtype=np.float32)
        liboled.init(arr)

    @parameterized.expand(
        [(i,) for i in [np.uint8, np.uint16, np.uint32, np.uint64, np.int8, np.int16, np.int32, np.int64]],
        custom_name_func
    )
    @unittest.skip("Might not need strict type checking")
    def test_can_not_take_other_types(self, _dtype):
        arr = np.random.random((liboled.OLED_HEIGHT, liboled.OLED_WIDTH, 3))
        with self.assertRaises(ValueError):
            liboled.init(arr)

    def test_get_buffer(self):
        liboled.init(self.arr)
        liboled.display()
        arr = liboled.get_buffer()
        expected_array = (self.arr * 256.).astype(np.uint8)
        expected_array[:, :, 0] = expected_array[:, :, 0] & 0xF8
        expected_array[:, :, 1] = expected_array[:, :, 1] & 0xFC
        expected_array[:, :, 2] = expected_array[:, :, 2] & 0xF8
        numpy.testing.assert_equal(expected_array, arr)


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

    @parameterized.expand([(i,) for i in [
        (liboled.OLED_HEIGHT - 1, liboled.OLED_WIDTH, 3),
        (liboled.OLED_HEIGHT - 1, liboled.OLED_WIDTH, 3),
        (liboled.OLED_HEIGHT + 1, liboled.OLED_WIDTH, 3),
        (liboled.OLED_HEIGHT, liboled.OLED_WIDTH - 1, 3),
        (liboled.OLED_HEIGHT, liboled.OLED_WIDTH + 1, 3),
        (liboled.OLED_HEIGHT, liboled.OLED_WIDTH, 2),
        (liboled.OLED_HEIGHT, liboled.OLED_WIDTH, 4),
    ]], custom_name_func_shape)
    def test_error_on_wrong_shape(self, shape):
        liboled.deinit()
        with self.assertRaises(ValueError):
            liboled.init(np.zeros(shape))

    def test_get_array(self):
        arr = liboled.get_array()
        numpy.testing.assert_equal(self.arr, arr)


if __name__ == '__main__':
    unittest.main()
