import sys

#argument 1 is the file name given by user
#argument 2 is the old file we are parsing to put into the history file
fileName = sys.argv[1]
oldFile = sys.argv[2]

newFile = "history_" + fileName

#the data we want to keep
labels = ['open directories', 'open databases', 'descend', 'sqlsum', 'sqlent', 'close databases', 'close directories', 'Real time']


with open(oldFile, 'r') as f:
    lines = f.readlines()

#we store the lines we want to keep
outputLines = []

for line in lines:
    #if there are any errors, don't record the performace times
    if "Error" in line:
        break
    for label in labels:
        if label in line:
            outputLines.append(line[45:-2])
            outputLines.append("\n")

#write the lines we wanted to keep to the file (unwanted lines are gone)
with open(newFile, 'a') as f:        
    for line in outputLines:
        f.write(line)

f = open(newFile, 'a')
f.write("\n")
f.close()
