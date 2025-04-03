from led import Led
from machine import Pin
from fifo import Fifo
import time

led = Led(22, mode=Pin.OUT)
brightness = 0
button = Pin(12, mode=Pin.IN, pull=Pin.PULL_UP)
status = False

class Encoder:
    def __init__(self, rot_a, rot_b):
        self.a = Pin(rot_a, mode = Pin.IN)
        self.b = Pin(rot_b, mode = Pin.IN)
        self.fifo = Fifo(30, typecode="i")
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        
    def handler(self, pin):
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)
        
rot = Encoder(10, 11)

while True:
    time.sleep(0.1)
    if button.value() == 0:
        print("b")
        time.sleep(0.10)
        while button.value() == 0:
            time.sleep(0.10)
        status = not status
        
        print("n")
    if rot.fifo.has_data():
        value = rot.fifo.get()
        if status == True:
            if value == 1:
                brightness = brightness + 1
            else:
                brightness = brightness - 1
    if status == True:
        led.on()
        led.brightness(brightness)
    else:
        led.off()
                
        
    
