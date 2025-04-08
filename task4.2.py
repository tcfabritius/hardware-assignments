from ssd1306 import SSD1306_I2C
from led import Led
from machine import Pin, I2C
import time
import micropython
from fifo import Fifo

micropython.alloc_emergency_exception_buf(200)

rb = fileFifo.Fifo(50, name='capture02_250Hz.txt')

