import unittest
import util
from unittest.mock import MagicMock
import time


class TestCache(unittest.TestCase):
    def test_cache_long(self):
        m = MagicMock()
        patched_function = util.max_update_rate(1e9)(m)

        m.assert_not_called()
        # Call the function twice, and check if it caches
        patched_function()
        patched_function()
        self.assertEqual(1, m.call_count)

    def test_cache_medium(self):
        m = MagicMock()
        timeout = 0.01
        patched_function = util.max_update_rate(timeout)(m)

        m.assert_not_called()
        # Call the function twice, and check if it caches
        patched_function()
        patched_function()
        self.assertEqual(1, m.call_count)

        time.sleep(timeout + 0.001)
        patched_function()
        self.assertEqual(2, m.call_count)
        patched_function()
        self.assertEqual(2, m.call_count)

    def test_cache_short(self):
        m = MagicMock()
        patched_function = util.max_update_rate(0)(m)

        # Call the function twice, and check if it caches
        patched_function()
        patched_function()
        self.assertEqual(2, m.call_count)


class TestIP(unittest.TestCase):
    def test_ip_is_sane(self):
        ips = util.get_ips()
        self.assertIsInstance(ips, tuple)
        for ip in ips:
            self.assertRegex(ip, r'^\d+\.\d+\.\d+\.\d+$')


if __name__ == '__main__':
    unittest.main()
