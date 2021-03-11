import unittest
from rotary_encoder import RotaryEncoder, PINS, GPIO
from unittest.mock import MagicMock, patch


class BaseGPIO_Test(unittest.TestCase):
    def setUp(self) -> None:
        patcher = patch("rpi.GPIO.input")
        self.input_mock = patcher.start()
        self.addCleanup(patcher.stop)
        self._pin_values = {PINS.CLK: False, PINS.DT: False, PINS.BTN: False}

        def get_pin_value(pin):
            if pin not in self._pin_values:
                raise ValueError(f"The pin {pin} has not been set before the test")
            return self._pin_values[pin]

        self.input_mock.side_effect = get_pin_value

    def set_pin(self, pin: PINS, val: bool):
        if pin not in self._pin_values:
            raise ValueError(f"The pin {pin} is not controlled by the mock")
        self._pin_values[pin] = val


class BaseTestRotaryEncoder(BaseGPIO_Test):
    def setUp(self) -> None:
        super().setUp()
        self.rotenc = RotaryEncoder()
        self.addCleanup(GPIO.cleanup)

        # Make sure we are at a known state first
        self.set_pin(PINS.CLK, False)
        self.rotenc.rotation_callback(PINS.CLK)


class TestSmoke(BaseTestRotaryEncoder):
    def test_calls_rotate_callback_on_clockwise(self):
        cb = MagicMock()
        self.rotenc.register_rotation_callback(cb)

        self.set_pin(PINS.CLK, True)
        self.rotenc.rotation_callback(PINS.CLK)
        cb.assert_called_with(True)


if __name__ == '__main__':
    unittest.main()
