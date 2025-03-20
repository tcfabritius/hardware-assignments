from ssd1306 import SSD1306_I2C
from machine import UART, Pin, I2C, Timer
import time
import micropython

ufoy=55
ufox=1

sw2 = Pin(7, Pin.IN, Pin.PULL_UP)
sw0 = Pin(9, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

oled.fill(0)
oled.text('<=>', ufox, ufoy, 1)
oled.show()
while True:
    if sw0():
        ufox = ufox + 1
        if ufox > 127:
            ufox = -5
        oled.fill(0)
        oled.text('<=>', ufox, ufoy, 1)
        oled.show()
    if sw2():
        ufox = ufox - 1
        if ufox < 0:
            ufox = 132
        oled.fill(0)
        oled.text('<=>', ufox, ufoy, 1)
        oled.show()

