from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import filedialog
import PIL
from PIL import ImageTk, Image, ImageDraw
import xml.etree.ElementTree as ET
import time

from time import gmtime, strftime
import glob
import threading
import os
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np

global dirSelect
dirSelect = 0

def clicked1():
    lbl.configure(text=entry1.get())

def selectDirectory():
    #dispImage = filedialog.askopenfilename(filetypes = (("Images","*.png"),("all files","*.*")))
    window.title("Cell Plotter GUI (Running . . . )")
    global winner
    global dir
    global cellCount
    winner = 0
    cellCount = 0
    dir = filedialog.askdirectory()
    print(dir)
    infoLabel1.configure(text="Directory: "+dir)
    os.chdir(dir)
    xmls = glob.glob("*.xml")
    pngs = glob.glob("*.png")
    diff = (len(pngs))-(len(xmls))
    place = str(len(xmls))+" ("+str(diff)+" unlabeled)"

    infoLabel2.configure(text="# images = "+str(len(pngs)))
    infoLabel3.configure(text="# annotations = "+place)

    for file in xmls:
        with open(file, 'r', encoding="utf-8") as content:
            tree = ET.parse(content)
            root = tree.getroot()
            for oj in root.findall('object'):
                cellCount +=1

    infoLabel4.configure(text="# cells = " + str(cellCount))
    cellCount =0

    im = Image.open(pngs[0])
    newImg = im.resize((320, 200), PIL.Image.ANTIALIAS)
    newImg3 = ImageTk.PhotoImage(newImg)
    w.configure(image=newImg3)
    w.image = newImg3


    window.title("Cell Plotter GUI")
    #infoLabel3.configure(text="")
    dirSelect = 1
   # newImg = Image.open(dispImage)
   # newImg = newImg.resize((320,240), PIL.Image.ANTIALIAS)
   # newImg3 = ImageTk.PhotoImage(newImg)
  #  w.configure(image=newImg3)
  #  w.image = newImg3


# def saveImg():
#     global imageCount
#     w.photo.write('yes.png',format='png')
#    # save = Image.open(w.photo)
#     #save.save("SavedPhoto" +str(imageCount0)+".png")
#   #  imageCount+=1


def plot():
    print("plotting")
    window.title("Cell Plotter GUI (Running . . . )")
    error = Label(window, text="Select a directory first")
    try:
        winner
    except NameError:
        print("oops")
        error.grid(column=2, row=2)
    cellPlot()

def cellPlot():
        error.grid_forget()
        numCellDots=int(entry1.get())
        print("Running cellPlot at :"+str(dir))
        os.chdir(dir)
        newDir = dir + "\\modseq" + str(numCellDots) + "_" + str(shortTime)
        os.mkdir(newDir)

        imgs = glob.glob("*.png")
        im = Image.open(imgs[0])
        im = im.convert('RGB')
        draw = ImageDraw.Draw(im)


        xminvalue = 0
        xmaxvalue = 0
        yminvalue = 0
        ymaxvalue = 0
        count = 0
        xmls = glob.glob("*.xml")
        numDots = 0
        #print("Plotting.....", end="", flush=True)

        pb = Progressbar(window, orient="horizontal", length=100, mode="indeterminate")
        pb.grid(column=2, row=4)

        for file in xmls:
            progress = int(100 * (xmls.index(file)) / len(xmls))
            name = os.path.basename(file)
            currfile = os.path.abspath(file)
            with open(file, 'r', encoding="utf-8") as content:
                tree = ET.parse(content)
                root = tree.getroot()
                for oj in root.findall('object'):
                    xmin = list(tree.iter('xmin'))
                    for value in xmin:
                        xminvalue = int(value.text)
                    #      print("xmin = " + str(xminvalue))

                    xmax = list(tree.iter('xmax'))
                    for value in xmax:
                        xmaxvalue = int(value.text)
                    #   print("xmax = " + str(xmaxvalue))

                    xmid = (xmaxvalue + xminvalue) / 2

                    ymin = list(tree.iter('ymin'))
                    for value in ymin:
                        yminvalue = int(value.text)
                    #    print("ymin = " + str(yminvalue))

                    ymax = list(tree.iter('ymax'))
                    for value in ymax:
                        ymaxvalue = int(value.text)
                    #  print("ymax = " + str(ymaxvalue))

                    ymid = (ymaxvalue + yminvalue) / 2

                    draw.point((xmid, ymid), fill=(190, 20, 20, 20))
                    numDots += 1
                    # print("new dot "+name+" num dots: "+str(numDots))

                count += 1
                if count % int(numCellDots) == 0:
                    # im.show()
                    draw.line([(0, 95), (int((count / len(xmls) * 160)), 95)], fill=220, width=4)
                    # os.chdir(dir+"\\"+str(numCellDots))
                    os.chdir(newDir)
                    im.save("part" + str(count / 100) + " " + str(numDots) + " dots.png")
                    os.chdir(dir)

                    del im
                    im = Image.open(imgs[0])
                    im = im.convert('RGB')
                    draw = ImageDraw.Draw(im)
                    # count=0
                    # print(str(numDots))
                    numDots = 0
        os.chdir(newDir)
        im.save("partLast.png")
        newImg = im.resize((320,200), PIL.Image.ANTIALIAS)
        newImg3 = ImageTk.PhotoImage(newImg)
        w.configure(image=newImg3)
        w.image = newImg3
        print("DONE")
        pb.grid_forget()
        window.title("Cell Plotter GUI")
        dirSelect = 0
        error.grid_forget()




shortTime = str(strftime("%m_%d_%H%M%S"))

#empty = "C:\\Users\\reidn\\Google Drive\\Owl\\Code\GRAFR\emptyrgb.png"
empty = "C:\\Users\\reidn\\Google Drive\\Owl\\Code\GRAFR\owl.jpg"
testImg = Image.open(empty)
testImg = testImg.resize((320,200), PIL.Image.ANTIALIAS)
#resized = empty.resize(320,200)
#dir = ""


window = Tk()
window.title("Cell Plotter GUI")
window.geometry('500x300')
#window.configure(background='grey')


image1 = Image.open(empty)
image1 = image1.resize((320,200),PIL.Image.ANTIALIAS)
dispImage = ImageTk.PhotoImage(image1)
w = Label(window,image=dispImage)
w.photo = dispImage
w.grid(column=2,row=2, rowspan = 3, padx=4, pady=4)

entryLabel = Label(window,text="# Cells / Picture", bg = 'yellow')
entryLabel.grid(column=4,row=3, sticky=W)

entry1 = Entry(window,width=5)
entry1.grid(column=3,row=3, padx=2, ipady = 3, ipadx=5, sticky =W)
entry1.insert(END,'200')

error = Label(window, text="Select a directory first")

infoLabel1 = Label(window,text= "Directory : ")
infoLabel1.grid(column=2,columnspan = 2, row=5, sticky=W)

infoLabel2 = Label(window,text= "# images : ")
infoLabel2.grid(column=2,columnspan = 2, row=6, sticky=W)

infoLabel3 = Label(window,text= "# annotations : ")
infoLabel3.grid(column=2,columnspan = 2, row=7, sticky=W)

infoLabel4 = Label(window, text="# cells = ")
infoLabel4.grid(column=2,columnspan = 2, row=8, sticky=W)


#pb = Progressbar(window,orient = "horizontal",length =100, mode = "indeterminate")
#pb.grid(column = 2, row =4)

btn2=Button(window,text='Select Directory',padx=3,pady=3, command=selectDirectory)
btn2.grid(column=3,row=2, padx = 10, ipady=10, columnspan=2, sticky=W)

startBtn = Button(window, text='Start Plotting', command=plot)
startBtn.grid(column=3,row=4, columnspan=2, sticky=W, padx=3)

# savebtn = Button(window, text="Save Image", command=saveImg)
# savebtn.grid(column=4,row=4, sticky=E, padx=40)


window.mainloop()
