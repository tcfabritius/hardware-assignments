from filefifo import Filefifo
from fifo import Fifo
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import micropython
from time import sleep_ms

micropython.alloc_emergency_exception_buf(200)

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

data = Filefifo(10, name='capture_250Hz_03.txt')

sampleCount = 1000

data_list = []

for _ in range(sampleCount):
    value = data.get()
    if value is not None:
        data_list.append(value)

minValue = min(data_list)
maxValue = max(data_list)

graph_width = oled_width
graph_height = oled_height - 10
y_values = [graph_height // 2] * graph_width
current_position = 0

def map_value(value, min_val, max_val, height):
    if min_val == max_val:
        return height // 2
    return height - int((value - min_val) / (max_val - min_val) * height)

class Encoder:
    def __init__(self, rot_a, rot_b, fifo):
        self.a = Pin(rot_a, mode=Pin.IN)
        self.b = Pin(rot_b, mode=Pin.IN)
        self.fifo = fifo
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)

    def handler(self, pin):
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)


def update_display():
    global current_position
    oled.fill(0)

    for i in range(graph_width):
        pos = current_position + i
        if pos < len(data_list):
            value = data_list[pos]
        else:
            value = minValue
        y_mapped = map_value(value, minValue, maxValue, graph_height)
        y_values[i] = y_mapped

    for i in range(1, graph_width):
        oled.line(i - 1, y_values[i - 1], i, y_values[i], 1)

    oled.show()

def process_encoder():
    global current_position
    while True:
        if not events.empty():
            move = events.get()
            new_position = current_position + (move * 10)

            if new_position < 0:
                new_position = 0

            if new_position + graph_width > sampleCount:
                new_position = sampleCount - graph_width 
                
            print(f"Move: {move}, Current Position: {current_position}, New Position: {new_position}")                

            current_position = new_position
            update_display()

        
events = Fifo(30, typecode='i')
rot = Encoder(10, 11, events)

print(f"Minimum value in data sample list is {minValue}.")
print(f"Maximum value in data sample list is {maxValue}.")

update_display()

process_encoder()
