from machine import Pin
import time
import micropython
from fifo import Fifo

micropython.alloc_emergency_exception_buf(200)
leds = [Pin(20, Pin.OUT), Pin(21, Pin.OUT), Pin(22, Pin.OUT)]
ledStates = [False, False, False]
menuIndex = 0
events = Fifo(30)

class InterruptButton:
    def __init__(self, button_pin, fifo):
        self.button = Pin(button_pin, mode=Pin.IN, pull=Pin.PULL_UP)
        self.lastPress = time.ticks_ms()
        self.fifo = fifo
        self.button.irq(handler=self.handler, trigger=Pin.IRQ_FALLING, hard=True)
    
    def handler(self, pin):
        now = time.ticks_ms()
        if time.ticks_diff(now, self.lastPress) > 50: #50ms cooldown
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
    print("\nMenu:")
    for i in range(3):
        if i == menuIndex:
            selected = "->" 
        else:
            selected = " "
        
        
        if ledStates[i]:
            status = "ON "     
        else:
            status = "OFF"
        
        
        print(f"{selected} LED{i+1}: {status}")

for i in range(3):
    ledStates[i] = leds[i].value()

rotFifo = Fifo(30)
rot = Encoder(10, 11, rotFifo)
button = InterruptButton(12, events)
updateMenu()

while True:
    if rotFifo.has_data():
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
