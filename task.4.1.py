import filefifo
import time

rb = filefifo.Filefifo(50, name = 'capture01_250Hz.txt')

last = 0
min = 9999999
max = 0
peakindexes = []
peakvalues = []
first_occurrence = True
averrange = 500
aver2range = 500
segmentid = 0
averages = []

for x in range(45000):
    if x < averrange:
        number = rb.get()
        if number < min:
            min = number
        if number > max:
            max = number
    else:
        average = (min + max)/2
        averages.append(average)
        averrange = averrange + 500
        min = 99999999
        max = 0


for x in range(45000):
    number = rb.get()
    if x < aver2range:
        aver = averages[segmentid]
    else:
        aver2range = aver2range + 500
        if segmentid < len(averages):
            segmentid = segmentid + 1
        
    if number - last < 0 and first_occurrence and number > aver:
        peakindexes.append(x)
        peakvalues.append(number)
        first_occurrence = False
            
    if number - last > 0:
        first_occurrence = True
    last = number
      
lastindex = peakindexes[0]
intervalInNumberOfSamples = []
for index in peakindexes:
    interval = index - lastindex
    if interval > 60:
        intervalInNumberOfSamples.append(interval)
    lastindex = index
    
bpm = []
for sample in intervalInNumberOfSamples:
    interval = sample / 250
    bpmv = int(60 / interval)
    bpm.append(bpmv)
    
for bpmv in bpm:
    print("BPM: " + str(bpmv))