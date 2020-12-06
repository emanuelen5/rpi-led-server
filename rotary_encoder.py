from RPi import GPIO
from time import sleep
from enum import IntEnum

class PINS(IntEnum):
    CLK = 5
    DT = 6
    BTN = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(PINS.CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PINS.DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PINS.BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

counter = 0
clkLastState = GPIO.input(PINS.CLK)

clkState = clkLastState = GPIO.input(PINS.CLK)
dtState = GPIO.input(PINS.DT)
def both_callback(channel):
    global clkState, clkLastState, dtState, counter
    btn = PINS(channel)
    value = GPIO.input(channel)
    if btn == PINS.CLK:
        clkState = value
    elif btn == PINS.DT:
        dtState = value
    else:
        print("Event for " + repr(btn) + f" with value={value}. Type: ", end="")

    clkState = GPIO.input(PINS.CLK)
    dtState = GPIO.input(PINS.DT)
    if clkState != clkLastState:
        if dtState != clkState:
            counter += 1
        else:
            counter -= 1
        print(f"Counter: {counter}")
    clkLastState = clkState

GPIO.add_event_detect(PINS.CLK, GPIO.BOTH, callback=both_callback)
GPIO.add_event_detect(PINS.DT,  GPIO.BOTH, callback=both_callback)
GPIO.add_event_detect(PINS.BTN, GPIO.BOTH, callback=both_callback)

try:
    while True:
        sleep(0.01)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
