from filefifo import Filefifo
from fifo import Fifo
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import micropython
from time import sleep_ms, ticks_ms, ticks_diff

micropython.alloc_emergency_exception_buf(200)

# === OLED Setup ===
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
GRAPH_HEIGHT = 54  # Below room for mode label
GRAPH_WIDTH = 128

# === Data and Display State ===
data = Filefifo(10, name='capture03_250Hz.txt')
data_list = []
current_position = 0
scale_factor = 0.01
offset = data.get()
minValue, maxValue = 0, 0

# === Pin Setup ===
sw0 = Pin(9, Pin.IN, Pin.PULL_UP)  # Offset
sw1 = Pin(8, Pin.IN, Pin.PULL_UP)  # Start
sw2 = Pin(7, Pin.IN, Pin.PULL_UP)  # Zoom
events = Fifo(30, typecode='i')  # Fifo with size of 30


# === Rotary Encoder ===
class Encoder:
    def __init__(self, a_pin, b_pin, fifo):
        self.a = Pin(a_pin, Pin.IN)
        self.b = Pin(b_pin, Pin.IN)
        self.fifo = fifo
        self.last_time = 0
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)

    def handler(self, pin):
        self.fifo.put(-1 if self.b() else 1)


rot = Encoder(10, 11, events)


# === Utility ===
def map_value(val, offset, scale, min_val, max_val, height):
    y = 63 - int((val - offset) * scale)
    return max(0, min(height - 1, y)) if max_val != min_val else height // 2


# === Load and Process Data ===
def load_grouped_data():
    raw = []
    grouped = []

    for _ in range(1800):
        val = data.get()
        if val is None:
            break
        raw.append(val)
        if len(raw) == 5:
            avg = sum(raw) // 5
            grouped.append(avg)
            raw = []

    return grouped


# === Display ===
def update_display(mode_label=""):
    oled.fill(0)

    if not data_list:
        oled.text("Press SW1", 30, 30)
    else:
        for x in range(GRAPH_WIDTH):
            idx = current_position + x
            if idx < len(data_list):
                val = data_list[idx]
                y = map_value(val, offset, scale_factor, minValue, maxValue, GRAPH_HEIGHT)
                if x > 0:
                    oled.line(x - 1, y_values[x - 1], x, y, 1)
                y_values[x] = y

        if mode_label:
            oled.text(mode_label, 0, GRAPH_HEIGHT + 1)

    oled.show()


# === Encoder Logic ===
def handle_encoder():
    global current_position, scale_factor, offset

    while True:
        # Check if events FIFO is not empty
        if not events.empty():
            move = events.get()

            # SW2 (Zoom) mode
            if not sw2.value():  # Zoom mode when SW2 is pressed
                scale_factor += move * 0.001  # Adjust zoom factor by 0.05
                print(f"Zoom: {scale_factor:.4f}")

            # SW0 (Offset) mode
            elif not sw0.value():  # Offset mode when SW0 is pressed
                offset += move * 100  # Adjust offset
                print(f"Offset: {offset}")

            # Default (Scroll) mode
            else:  # Scroll mode when no button is pressed
                current_position += move * 5
                current_position = max(0, min(len(data_list) - GRAPH_WIDTH, current_position))
                print(f"Scroll: {current_position}")

        if events.empty():
            update_display()

# === Main Program ===

# Wait for SW1
while sw1.value():
    update_display()
    sleep_ms(50)

# Load and group data
data_list = load_grouped_data()
sample_count = len(data_list)
y_values = [GRAPH_HEIGHT // 2] * GRAPH_WIDTH

if sample_count > 0:
    minValue = min(data_list)
    maxValue = max(data_list)
    print(f"Loaded {sample_count} samples.")
    print(f"Min: {minValue}, Max: {maxValue}")
else:
    print("No data loaded.")

# Initial display
update_display("Ready")

# Start handling encoder
handle_encoder()
