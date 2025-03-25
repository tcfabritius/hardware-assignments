from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
import time

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

yPos = 0  
fontSize = 8

oled.fill(0)
oled.show()

while True:
    givenInput = input("Type something will ya: ")
    
    if yPos + fontSize > 63:
        oled.scroll(0, -fontSize)
        oled.fill_rect(0, 56, 128, 8, 0)
        yPos = 56
    else:
        yPos += fontSize

    oled.text(givenInput, 0, yPos)
    oled.show()

