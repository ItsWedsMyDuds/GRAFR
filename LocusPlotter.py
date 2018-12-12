import os
import glob
import shutil
from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET
from time import gmtime, strftime
print("Program start")
import cv2

#os.chdir("C:\\Users\\reidn\\Desktop\\T87 1120\\all")
#os.chdir("C:\\Users\\reidn\\Desktop\\Coding\\CellPlot\\Test1")
#os.chdir("C:\\Users\\reidn\\Desktop\\Coding\\CellPlot\\Test2")
#os.chdir("C:\\Users\\reidn\\Desktop\\T87 1120\\all_png 5 percent\\firstdrop")
#os.chdir("C:\\Users\\reidn\\Desktop\\T87 1120\\all_png 5 percent\\test")
shortTime = str(strftime("%m_%d_%H%M%S"))
print("input directory")
dir = input()
print("number of cells per image")
numCellDots = input()

os.chdir(dir)
newDir = dir+"\\modseq"+str(numCellDots)+"_"+str(shortTime)
os.mkdir(newDir)

imgs = glob.glob("*.png")
im = Image.open(imgs[0])
im = im.convert('RGB')

#draw = ImageDraw.Draw(im)
drawMedian = ImageDraw.Draw(im)

#draw.point((20,20),255)
#im.show()

xminvalue = 0
xmaxvalue = 0
yminvalue = 0
ymaxvalue = 0
xsum = 0
ysum = 0
count = 0
counter = 0
xmls = glob.glob("*.xml")
numDots=0

print("Plotting.....",end="",flush=True)

for file in xmls:
    name = os.path.basename(file)
    #print("Current File = "+name)
    #print(name+str(os.path.getctime(file)))
    currfile = os.path.abspath(file)
    with open(file,'r',encoding="utf-8") as content:
        tree = ET.parse(content)
        root = tree.getroot()
        for oj in root.findall('object'):
            counter +=1
            xmin = list(tree.iter('xmin'))
            for value in xmin:
                xminvalue = int(value.text)
          #      print("xmin = " + str(xminvalue))

            xmax = list(tree.iter('xmax'))
            for value in xmax:
                xmaxvalue = int(value.text)
             #   print("xmax = " + str(xmaxvalue))

            xmid = (xmaxvalue+xminvalue)/2
            xsum = xsum + xmid

            ymin = list(tree.iter('ymin'))
            for value in ymin:
                 yminvalue = int(value.text)
            #    print("ymin = " + str(yminvalue))

            ymax = list(tree.iter('ymax'))
            for value in ymax:
                ymaxvalue = int(value.text)
              #  print("ymax = " + str(ymaxvalue))

            ymid = (ymaxvalue+yminvalue)/2
            ysum = ysum + ymid


            #draw.point((xmid, ymid), fill=(190,20,20,20))

            numDots +=1
            #print("new dot "+name+" num dots: "+str(numDots))

        count+=1
        if count %int(numCellDots) == 0:
                #im.show()
            drawMedian.line([(0, 95), (int((count / len(xmls) * 160)), 95)], fill=220, width=4)
            drawMedian.point((xsum/counter, ysum/counter), fill=(190, 20, 20, 20))
            xsum = 0
            ysum = 0
            counter = 0
            os.chdir(newDir)
            im.save("part "+str(count/100)+" median.png")
            os.chdir(dir)


            del im

            os.chdir(dir)
            im = Image.open(imgs[0])
            im = im.convert('RGB')
            drawMedian = ImageDraw.Draw(im)

            numDots=0

#
os.chdir(newDir)
im.save("partLastMedian.png")
# print("generating video")
#
# video_name = 'test.avi'
# newPics = glob.glob("*.png")
# frame = cv2.imread(os.path.join(newDir,newPics[0]))
# height, width, layers = frame.shape
#
# video = cv2.VideoWriter(video_name, -1, 1, (width, height))
# for file in newPics:
#     video.write(file)
#
# cv2.destroyAllWindows()
# video.release()

print("DONE")
#im.show()
#im.show()