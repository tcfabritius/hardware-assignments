from ssd1306 import SSD1306_I2C
from led import Led
from machine import Pin, I2C
import time
import micropython
from fifo import Fifo

micropython.alloc_emergency_exception_buf(200)
brightness = 5
leds = [Led(20, mode=Pin.OUT), Led(21, mode=Pin.OUT), Led(22, mode=Pin.OUT)]
ledStates = [False, False, False]
menuIndex = 0
events = Fifo(30)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

class InterruptButton:
    def __init__(self, button_pin, fifo):
        self.button = Pin(button_pin, mode=Pin.IN, pull=Pin.PULL_UP)
        self.lastPress = time.ticks_ms()
        self.fifo = fifo
        self.button.irq(handler=self.handler, trigger=Pin.IRQ_FALLING, hard=True)
    
    def handler(self, pin):
        now = time.ticks_ms()
        if time.ticks_diff(now, self.lastPress) > 250: #50ms cooldown
            self.lastPress = now
            self.fifo.put(0)

class Encoder:
    def __init__(self, rot_a, rot_b, fifo):
        self.a = Pin(rot_a, mode=Pin.IN)
        self.b = Pin(rot_b, mode=Pin.IN)
        self.fifo = fifo
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)

    def handler(self, pin):
        if self.b.value():
            #Left
            self.fifo.put(-1)
        else:
            #Right
            self.fifo.put(1)

def updateMenu():
    oled.fill(0)
    print("\nMenu:")
    for i in range(3):
        leds[i].brightness(brightness)
        if i == menuIndex:
            selected = "<3"
        else:
            selected = "  "
        
        if ledStates[i]:
            status = "ON"
        else:
            status = "OFF"
        
        feed = f"{selected} LED{i+1}: {status}"
        oled.text(feed, 1, i*10, 1)
        oled.show()

for i in range(3):
    ledStates[i] = leds[i].value()

rotFifo = Fifo(30, typecode='i')
rot = Encoder(10, 11, rotFifo)
button = InterruptButton(12, events)
updateMenu()

while True:        
    if rotFifo.has_data():
        while rotFifo.has_data():
            menuIndex = (menuIndex + rotFifo.get()) % 3
        updateMenu()

    if events.has_data():
        event = events.get()
        if event == 0:
            ledStates[menuIndex] = not ledStates[menuIndex]
            leds[menuIndex].value(ledStates[menuIndex])
            
            if ledStates[menuIndex]:
                print(f"Button pressed! LED{menuIndex+1} ON")
            else:
                print(f"Button pressed! LED{menuIndex+1} OFF")
            
            updateMenu()
