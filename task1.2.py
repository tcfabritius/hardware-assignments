from ssd1306 import SSD1306_I2C
from machine import UART, Pin, I2C, Timer, ADC
import fifo
import time
import micropython
micropython.alloc_emergency_exception_buf(200)

button = Pin(9, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)
rb = fifo.Fifo(50)
listOfThings =[]

if rb.empty():
    print('Fifo is empty')

led = Pin("LED", Pin.OUT)
oled.fill(0)

while True:
    givenInput = input("Type something will ya\nSomething: ")
    oled.text(givenInput,1,1,1)
    oled.show()
    oled.scroll(0,10)
    oled.rect(1,1,8,8,0,True)
    time.sleep(1)

# if rb.empty():
#     print('Fifo is empty')
# 
# led = Pin("LED", Pin.OUT)
# oled.fill(0)
# 
# while True:
#     givenInput = input("Type something will ya\nSomething: ")
#     listOfThings.append(givenInput)
#     #print(listOfThings)
#     for i in listOfThings:
#         oled.text(i,1,1,1)
#         oled.show()
#         oled.scroll(0,10)
#         time.sleep(1)

