[![Build Python Package status badge](https://github.com/emanuelen5/rpi-led-server/actions/workflows/python.yml/badge.svg)](https://github.com/emanuelen5/rpi-led-server/actions/workflows/python.yml)

# Raspberry Pi LED server
This project will serve as an LED server that connects to external services through Ethernet and fetches data which can then be shown through the means of an LED light show.

## [Hardware](./doc/hardware.md)

* **Raspberry Pi**
  
  The compute platform

* **RGB LEDs**
  
  For displaying notifications

* **SSD1331 OLED screen**
  
  For showing current LED mode and IP

* **Rotary Encoder**
  
  For setting brightness and changing LED mode

### Fritzing model
![Fritzing breadboard design](doc/rpi-leds-and-screen_bb.png)

### Assembled prototype
![Assembled protoype header](doc/prototype-assembled.jpg)

## Application

* **Display (controlled through Python C interface) that shows the current status**
* **Flask server (coming) that reacts to web requests**
