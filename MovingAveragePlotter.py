##Generates moving average graph



import matplotlib.pyplot as plt
import os
import numpy as np


#mainDir = "C:\\Users\\reidn\\Desktop\\Coding\\Matplotlib\\test"
#os.chdir(mainDir)


def movingAverage(csvName,movAvg = 20):


    print("Generating graph.....", end="", flush=True)

    csv = np.genfromtxt(csvName, dtype='int', delimiter=',')

    length = np.arange(0, len(csv), 1)

    movingAverageList = []
    timePointList = []
    count = 0
    tempSum = 0
    for value in csv:
        #if value.index(csv)==0:
            #continue
        tempSum = tempSum + value
        count += 1
        if count % movAvg == 0:
            avg = tempSum / movAvg
            tempSum = 0
            movingAverageList.append(avg)
            timePointList.append(count)

    plt.figure(1)
    plt.subplot(211)
    plt.plot(length,csv,'k')
    plt.ylabel('Avg Confidence Score (%)')


    plt.subplot(212)
    plt.plot(timePointList, movingAverageList,'k')
    # plt.plot(length,x)
    plt.ylabel('Moving Average ('+str(movAvg)+')')
    plt.savefig("figure_movAvg="+str(movAvg)+".png")
    plt.savefig("figure_movAvg="+str(movAvg)+".svg")
    plt.show()


print("Input directory of file")
mainDir = input()
print("Input file name (include .csv)")
file = input()
print("Input moving average window")
window = input()
print("At directory: "+mainDir)
print("File name: "+file)
print("Moving window: "+window)
os.chdir(mainDir)
movingAverage(file,movAvg = int(window))
print("DONE")