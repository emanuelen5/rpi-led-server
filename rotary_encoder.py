from RPi import GPIO
from time import sleep
from enum import IntEnum

class PINS(IntEnum):
    CLK = 5
    DT = 6
    BTN = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(PINS.CLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PINS.DT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PINS.BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0
clkLastState = GPIO.input(PINS.CLK)

def my_callback(channel):
    print(f"Callback on {channel}")

GPIO.add_event_detect(PINS.CLK, GPIO.BOTH, callback=my_callback, bouncetime=20)
GPIO.add_event_detect(PINS.DT, GPIO.BOTH, callback=my_callback, bouncetime=20)
GPIO.add_event_detect(PINS.BTN, GPIO.BOTH, callback=my_callback, bouncetime=20)

try:
    while True:
        clkState = GPIO.input(PINS.CLK)
        dtState = GPIO.input(PINS.DT)
        if clkState != clkLastState:
            if dtState != clkState:
                counter += 1
            else:
                counter -= 1
            print(f"Counter: {counter}")
        clkLastState = clkState
        sleep(0.01)
finally:
    GPIO.cleanup()
