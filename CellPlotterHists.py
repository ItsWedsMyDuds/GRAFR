import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import cv2
import pandas as pd
import os
import numpy as np
import glob
from natsort import natsorted, ns
global fileDir
import statistics
from statistics import stdev
from fractions import Fraction as fr
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from matplotlib.ticker import NullFormatter
import PIL
from PIL import Image, ImageDraw
from pprint import pprint


dir = "C:\\Users\\reidn\\Desktop"
#dir = "D:\\Processing\\Ozone\\201812131522\\cell"
#dir = "D:\\Processing\\Ozone\\201812131105\\cell"
os.chdir(dir)
file = "C:\\Users\\reidn\\Desktop\\cellStats\\cell_details.xlsx"
#file = "D:\\Processing\Ozone\\201812131522\\cell\\cell_details.xlsx"
#file = "D:\\Processing\\Ozone\\201812131105\\cell\\cell_details.xlsx"
df = pd.read_excel(file)
#print(df.columns)
xVals = df['X Pos'].values
yVals = df['Y Pos'].values


count = 0
xlist = []
ylist = []
xStds = []
ylist = []
yStds = []
xInts = []
yInts = []
print("Plotting.....",end="",flush=True)
for val in xVals:
    count+=1
    if val == "-":
        continue
    if count%50 == 0:
        xStds.append(statistics.stdev(xlist))
        #print(statistics.stdev(xlist))
        #print(count)
        xlist = []
    #count +=1
    xlist.append(int(val))
    xInts.append(int(val))
for val in yVals:
    count+=1
    if val == "-":
        continue
    if count%50 == 0:
        yStds.append(statistics.stdev(ylist))
        #print(statistics.stdev(ylist))
        #print(count)
        ylist = []
    #count +=1
    ylist.append(int(val))
    yInts.append(int(val))
print("DONE")

#axes definitions - sets location and dimension of axes
# then creates them with plt.axes
left, width = 0.1, 0.6
bottom, height = 0.1, 0.45
bottom_h = left_h = left + width + 0.02

rect_scatter = [left, bottom, width, height]
rect_histx = [left, bottom_h-0.1, width, 0.22]
rect_histy = [left_h, bottom, 0.2, height]

axScatter = plt.axes(rect_scatter)

plt.xlim(0,160)
plt.grid(True)
plt.axis([0,160,100,0])

axHistx = plt.axes(rect_histx)
plt.axis([0,160,0,len(xInts)])

axHisty = plt.axes(rect_histy)
plt.axis([0,(len(yInts)/2),100,0])

np.savetxt('xints.csv',xInts,delimiter=',', fmt='%s')
np.savetxt('yints.csv',yInts,delimiter=',', fmt='%s')


nullfmt = NullFormatter() #removes formatting from axes
#axHisty.xaxis.set_major_formatter(nullfmt)
axHisty.yaxis.set_major_formatter(nullfmt)



axScatter.scatter(xInts,yInts, alpha = 0.2)

axHisty.hist(yInts, orientation=u'horizontal')
axHistx.hist(xInts)
#axHistx.xlim(0,160)
#print(axScatter.ylim())

plt.figure(1, figsize=(4,3.5))
#img = mpimg.imread('owl.png')
#imgplot = plt.imshow(img)
plt.show()
