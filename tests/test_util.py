import unittest
import util


class TestIP(unittest.TestCase):
    def test_ip_is_sane(self):
        ip = util.get_ip()
        self.assertRegex(ip, r'^\d+\.\d+\.\d+\.\d+$')


if __name__ == '__main__':
    unittest.main()
