from filefifo import Filefifo
from machine import Pin
import time
import micropython
micropython.alloc_emergency_exception_buf(200)
from fifo import Fifo

class Interrupt_button:
    def __init__(self, button_pin, fifo):
        self.button = Pin(button_pin, mode = Pin.IN, pull = Pin.PULL_UP)
        self.nr = button_pin
        self.fifo = fifo
        self.button.irq(handler = self.handler, trigger = Pin.IRQ_FALLING, hard = True)

    def handler(self, pin):
        self.fifo.put(self.nr)

events = Fifo(30)

sw0 = Interrupt_button(9, events)
sw1 = Interrupt_button(8, events)
sw2 = Interrupt_button(7, events)

while True:
    if events.has_data():
        print(events.get())


# class Button_handler:
#     def __init__(self, indicator_led):
#         self.led = Pin(indicator_led, Pin.OUT)
#         self.count = 0
# 
#     def handler(self, pin):
#         self.count += 1
#         self.led.toggle()
# 
# button = Pin(9, mode = Pin.IN, pull = Pin.PULL_UP)
# my_button = Button_handler(22)
# 
# button.irq(handler = my_button.handler, trigger = Pin.IRQ_FALLING, hard = True)
# old = 0
# 
# while True:
#     if old != my_button.count:
#         old = my_button.count
#         print("Button count:", old)

 
# button = Pin(9, mode = Pin.IN, pull = Pin.PULL_UP)
# led = Pin("LED", Pin.OUT)
# pressed = False
# 
# def button_handler(pin):
#     led.toggle()
#     
# button.irq(handler = button_handler, trigger = button.IRQ_FALLING, hard = True)
#     
# while True:
#     if pressed:
#         pressed = True
#         print ("Button was pressed.")