from filefifo import Filefifo
data = Filefifo(10, name = 'capture_250Hz_03.txt')

last = 0
peakindexes = []
peakvalues = []
first_occurrence = True
for x in range(2653):
    number = data.get()
    if number - last < 0 and first_occurrence:
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
    
intervalInSeconds = []
for sample in intervalInNumberOfSamples:
    interval = sample / 250
    intervalInSeconds.append(interval)
    
for intervalSample in intervalInNumberOfSamples:
    print("Interval in samples " + str(intervalSample))
    
for intervalSecond in intervalInSeconds:
    print("Interval in seconds " + str(intervalSecond))
    
if intervalInSeconds:
    averageinterval = sum(intervalInSeconds) / len(intervalInSeconds)
    frequence = 1 / averageinterval
    print("Frequence is " + str(frequence) + " Hz")

