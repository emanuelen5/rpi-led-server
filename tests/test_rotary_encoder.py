import unittest
from rotary_encoder import RotaryEncoder, PINS, GPIO
from unittest.mock import MagicMock, patch


class TestSmoke(unittest.TestCase):
    def setUp(self) -> None:
        self.rotenc = RotaryEncoder()
        self.pin_values = {PINS.CLK: False, PINS.DT: False, PINS.BTN: False}

    def tearDown(self) -> None:
        GPIO.cleanup()

    @patch("rotary_encoder.GPIO.input")
    def test_calls_rotate_callback_on_clockwise(self, input_mock: MagicMock):
        cb = MagicMock()

        def get_pin_value(pin):
            return self.pin_values[pin]

        input_mock.side_effect = get_pin_value
        self.rotenc.register_rotation_callback(cb)

        # Make sure we are at a known state first
        self.pin_values[PINS.CLK] = False
        self.rotenc.rotation_callback(PINS.CLK)

        # Now run test
        self.pin_values[PINS.CLK] = True
        self.rotenc.rotation_callback(PINS.CLK)
        cb.assert_called_with(True)


if __name__ == '__main__':
    unittest.main()
