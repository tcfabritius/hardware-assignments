from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
import time
from filefifo import Filefifo
import micropython

micropython.alloc_emergency_exception_buf(200)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
rb = Filefifo(50, name='capture02_250Hz.txt')
#rb = Fifo(50)
#Interruption and filehandler to make it compatible with crowtail

def scaler(value, minVal, maxVal):
    if maxVal == minVal:
        return 32
    scaled = int((value - minVal) * 63 / (maxVal - minVal))
    return min(max(scaled, 0), 63)

while True:
    minVal = None
    maxVal = None
    count = 0
    while count < 250:
        if rb.has_data():
            sample = rb.get()
            if minVal is None or sample < minVal:
                minVal = sample
            if maxVal is None or sample > maxVal:
                maxVal = sample
            count += 1

    oled.fill(0)
    prevX = None
    prevY = None
    x = 0
    sumVal = 0
    samples = 0

    while x < 128:
        if rb.has_data():
            sample = rb.get()
            sumVal += sample
            samples += 1

            if samples == 5:
                avg = sumVal / 5
                y = 63 - scaler(avg, minVal, maxVal)
                if prevX == None:
                    prevX = x
                    prevY = y
                oled.line(x,y,prevX,prevY,1)
                prevX = x
                prevY = y
                sumVal = 0
                samples = 0
                x += 1
    oled.show()
    time.sleep(0.1)
