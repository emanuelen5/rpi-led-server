# Hardware
Here are some details on the design / content of the actual hardware.

## Parts

* Raspberry Pi
* Neopixels
* A 96x64 pixel color SSD1331 OLED screen (for showing current LED mode and IP)
* Rotary Encoder (for setting brightness and changing LED mode)
* MOSFET
* Some resistors
* Female 2.54mm headers

## Prototype
The hardware prototype is done as a Fritzing design. I designed two custom parts in Inkscape for the *rotary encoder* and the *SSD1331 OLED screen*.

### Fritzing parts
The fritzing catalogue contains a schematic + visual hookup for the prototype as well as the custom fritzing libraries for the encoder and display:

* [Prototype hookup](../fritzing/rpi-leds-and-screen.fzz)
  * [Rotary encoder part](../fritzing/local-library/rotary-encoder)
  * [SSD1331 display part](../fritzing/local-library/ssd1331)

## Assembly
I used female headers for three things:

* Connecting to the Rasperry Pi male header
* Connecting to the breakout modules (rotary encoder and OLED)
* Giving mechanical support underneath the button (so that the board doesn't flex too much when the button is pressed)

The thought was to make it easy to disassemble and replace parts.
