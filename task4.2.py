import time
from fifo import Fifo

micropython.alloc_emergency_exception_buf(200)

rb = fileFifo.Fifo(50, name='capture02_250Hz.txt')

for _ in range (100):
    if rb.has_data():
        print(rb.get())

