from filefifo import Filefifo
import time
import micropython

data = Filefifo(10, name = 'capture_250Hz_02.txt')

sampleFreq = 250
sampleCount = 2*sampleFreq

minValue = data.get()
maxValue = minValue

for _ in range(sampleCount-1):
    value = data.get()
    
    if value < minValue:
        minValue = value
        
    if value > maxValue:
        maxValue = value

print('min value is: ', minValue)
print('max value is: ', maxValue)

total = 10*sampleFreq

for _ in range(total):
    value = data.get()
    plotValue = (value-minValue)/(maxValue-minValue)*100
    print(plotValue)

        
    
    




