import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

# button setup
up_button = Pin(7, Pin.IN, Pin.PULL_UP)
clear_button = Pin(8, Pin.IN, Pin.PULL_UP)
down_button = Pin(9, Pin.IN, Pin.PULL_UP)

# screen setup
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

# Initial variables
x = 0
y = 30

while True:
    # clear screen
    if clear_button.value() == 0:
        oled.fill(0)
        x = 0
        y = 30
        oled.show()

    # move up
    if up_button.value() == 0:
        y -= 1
        if y < 0:
            y = 0 

    # move down
    if down_button.value() == 0:
        y += 1
        if y >= oled_height:
            y = oled_height - 1

    # drawing
    oled.pixel(x, y, 1) 
    oled.show()

    x += 1  # moves the line forward
    if x >= oled_width:  # wrap line around
        x = 0  

    time.sleep(0.05)
