import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import time
import re
from copy import deepcopy
from matplotlib.widgets import Slider



def grabDataThigh(filename : str,header=1):
    df = pd.read_csv(filename,header=header)
    dfThigh = df.loc[df["type"]=="t"]
    return dfThigh


def fixTimeData(df : pd.DataFrame):
    data = deepcopy(df)
    datadict = data.to_dict("list")
    timeValues = []
    x = datadict["time"]
    for i in range(len(x)):
        xValues = re.findall(r'[0-9.]+',x[i])
        tmpTime = 360*float(xValues[0])
        tmpTime = tmpTime + 60*float(xValues[1])
        tmpTime = tmpTime + float(xValues[2])
        timeValues.append(tmpTime)
    datadict["time"] = timeValues
    
    return datadict

def splitData(df : dict, start, stop):
    datadict = deepcopy(df)
    x = datadict["time"]
    startCheck = True
    endCheck = False
    if isinstance(start,int) and isinstance(stop,int):
        for i in range(len(x)):
            if x[i] < start and startCheck:
                pass
            elif x[i] >= start and startCheck:
                tmpStart = i
                startCheck = False
                endCheck = True
            elif x[i] < stop and endCheck:
                pass
            elif x[i] >= stop and endCheck:
                tmpStop = i
                endCheck = False
        dataFrame = pd.DataFrame(datadict)
        splitDict = dataFrame[tmpStart:tmpStop]
        splitDict.to_csv("JonasWalk6min.csv")
    else:
        tmpStart = []
        tmpStop = []
        for j in range(len(start)):
            startCheck = True
            endCheck = False
            for i in range(len(x)):
                if x[i] < start[j] and startCheck:
                    pass
                elif x[i] >= start[j] and startCheck:
                    tmpStart.append(i)
                    startCheck = False
                    endCheck = True
                elif x[i] < stop[j] and endCheck:
                    pass
                elif x[i] >= stop[j] and endCheck:
                    tmpStop.append(i)
                    endCheck = False
        dataFrame = pd.DataFrame(datadict)
        splitDict = {}
        for i in range(len(start)):
            dataFrame[tmpStart[i]:tmpStop[i]].to_csv(f"JonasWalk6min.csv")
        

def plotFSRData(data : dict):
    data = list(data.items())
    y = []
    for i in range(len(data)):
        if i == 0:
            x = data[i][1]
        if "FSR" in data[i][0]:
            y.append(data[i][1])
    return x, y

def plotGyroLiAccData(data : dict):
    data = list(data.items())
    y = []
    tmpCutStart = None
    tmpCutEnd = None

    for i in range(3,len(data[2][1])-10):
        if i < len(data[13][1])/2 and tmpCutStart == None:
            if len(set(data[13][1][i-3:i])) != 3:
                tmpCutStart = i-3
        elif i > len(data[13][1])/2 and tmpCutEnd == None:
            if len(set(data[13][1][i:i+10])) == 1:
                tmpCutEnd = i


    for i in range(len(data)):
        if i == 0:
            x = data[i][1]#[tmpCutStart:tmpCutEnd]
        if 13<=i<=15:
            y.append(data[i][1])#[tmpCutStart:tmpCutEnd])
        if 20<=i<=22:
            y.append(data[i][1])#[tmpCutStart:tmpCutEnd])
    '''
    checkRange = 20
    for i in range(checkRange,len(y[3])-checkRange):
        if sum(abs(number) for number in y[3][i-checkRange:i])/checkRange<1 and sum(abs(number) for number in y[4][i-checkRange:i])/checkRange<1 and sum(abs(number) for number in y[5][i-checkRange:i])/checkRange<1:
            print(f"Standing Still at {x[i]}")
    
    k = 0
    for i in range(len(x)):
        if x[i-k] < 12:
            x.pop(i-k)
            for j in range(len(y)):
                y[j].pop(i-k)
            k = k+1
        elif 32< x[i-k] <35:
            x.pop(i-k)
            for j in range(len(y)):
                y[j].pop(i-k)
            k = k+1
        elif 47 < x[i-k]:
            x.pop(i-k)
            for j in range(len(y)):
                y[j].pop(i-k)
            k = k+1
    '''

    fig, ax = plt.subplots(3,3,sharey="col",sharex="col")
    tmp = []
    for i in range(3):
        y.append([y[i][j] * y[i+3][j] for j in range(len(y[i]))])

    

    for i in range(3):
        ax[i,0].plot(x,y[i], label = f"Gyro {(i+1)%3}")
    
        ax[i,1].plot(x,y[i+3], label = f"Linear Acceleration {(i+1)%3}")
        
        ax[i,2].plot(x,y[i+6], label = f"LiAcc * Gyro {(i+1)%3}")
    ax[0,0].set_title("Gyro Measurements \n X")
    ax[0,1].set_title("Linear Acceleration Measurements \n X")
    ax[1,0].set_title("Y")
    ax[1,1].set_title("Y")
    ax[2,0].set_title("Z")
    ax[2,1].set_title("Z")
    fig.legend()
    plt.show()

start = [1.5]
stop = [313.1]
filename = "Code\Data\Jonas 6 min.txt"
with open(filename) as f:
    firstline = f.readline()
    f.close()
print(firstline)
sampleRate = re.findall(r'\d+\.\d+',firstline)
df = grabDataThigh(filename,0)
data = df.to_dict("list")
#data = fixTimeData(df)

x, y = plotFSRData(data)
for i in y:
    plt.plot(x,i)

plt.show()
#splitData(data, start,stop)
#plotGyroLiAccData(data)

'''
size = 500
plt.ion()
figure, ax = plt.subplots(figsize=(10, 8))  
for i in range(len(x)):
    x_value = re.findall(r'\d+\.\d+',x[i])
    x[i] = float(x_value[0])
linelist = []
for j in range(len(y)):
    if j > 2:
        line = ax.plot(x,y[j], label = f"Gyro {(j+1)%3}")
        linelist.append(line)
    else:
        line = ax.plot(x,y[j], label = f"Linear Acceleration {(j+1)%3}")
        linelist.append(line)
    print(j)

t1 = x[0]
t2 = x[500]
sec = t2-t1

# print(sec, size/float(sampleRate[0]))
# setting title
plt.title("Geeks For Geeks", fontsize=20)
plt.subplots_adjust(bottom=0.25)
plt.legend()
# setting x-axis label and y-axis label
plt.xlabel("X-axis")
plt.ylabel("Y-axis")

while 1:
    for j in range(len(y)):
        line = linelist[j]
        line[0].set_ydata(y[j])#[i*20:(i*20)+size])
    # drawing updated values
    figure.canvas.draw()
 
    # This will run the GUI event
    # loop until all UI events
    # currently waiting have been processed
    figure.canvas.flush_events()
    time.sleep(1)
    if (i*20)+size > len(x):
        i=0
    else:
        i = i+1
'''