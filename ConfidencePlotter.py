
###############################################################################################################
#                                       CONFIDENCE PLOTTER
###############################################################################################################

#Plots Self-Aware reported sort efficiency and purity to annotation confidence

# 1 Get average confidence of all bounding boxes in an annotation file
# 2 Link these average scores to an XML file name
    # Dictionary
# 3 Get names of XMLs and compare to PNGs
    # Dictionary
# 4 Take associated PNGs and get creation time
# 5 Match times to names of PNGs
# 6 Plot everything

#12.7 Finished transfering

#TODO
#Cell location plotting
#Graph plotting

###############################################################################################################
###############################################################################################################

##IMPORTS

import os
import glob
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw
import csv
import time
from time import gmtime, strftime

currentTime = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
shortTime = str(strftime("%m_%d_%H%M%S"))
print("Program Start "+currentTime)


totalScore = 0
scoreList = []
scoreDict = {}
xmlList = []
pngList = []
matchPngList = []
createTimeList = []
finalList = []
finalDict  = {}
#1
def get_confidence():
    os.chdir(mainDir)
    totalScore = 0
    xmls = glob.glob("*.xml")
    print("Getting average confidence.....",end="",flush=True)

    for file in xmls:
        name = os.path.basename(file)
        fileTemp = name.rsplit('.',1)
        fileName = fileTemp[0]
        with open(file, 'r', encoding="utf-8") as content:
            tree = ET.parse(content)
            root = tree.getroot()
            score = list(tree.iter('score'))
            if score != 0:
                for value in score:
                    scorevalue = int(round(float(value.text)))
                    totalScore += scorevalue
                totalScore = int(totalScore / int(len(score)))
                scoreList.append(totalScore/100)
                scoreDict[fileName] = totalScore
                totalScore = 0
    os.chdir(fileDir)
    np.savetxt("scoreList.csv", scoreList, delimiter=",", fmt='%s')
    with open("scoreDict.csv",'w') as f:
        fieldNames = ['File','AvgConfidence']
        writer = csv.DictWriter(f,fieldnames=fieldNames)
        writer.writeheader()
        data = [dict(zip(fieldNames,[k,v]))for k,v in scoreDict.items()]
        writer.writerows(data)
#2, 3
def xml_confidences():
    print("Comparing annotations to PNGs.....", end="", flush=True)
    xmlList = list(scoreDict.keys())
    os.chdir(fileDir)
    np.savetxt("xmls.csv", xmlList, delimiter=",", fmt='%s')
    os.chdir(mainDir)
    pics = glob.glob("*.png")
    for pic in pics:
        picname = os.path.basename(pic)
        picsplitlist = picname.rsplit('.', 1)
        picbase = picsplitlist[0]
        pngList.append(picbase)

    matchSet = set(pngList) & set(xmlList)
    matchList = list(matchSet)
    matchList.sort()
    os.chdir(fileDir)
    np.savetxt("AnnotatedPics.csv",matchList,delimiter=",",fmt='%s')

    for pic in matchList:
        picFile = pic+".png"
        matchPngList.append(picFile)
#4
def picture_time():
    print("Getting PNG creation time.....", end="", flush=True)
    os.chdir(mainDir)
    for item in matchPngList:
        picname = os.path.basename(item)
        if item == picname:
            ctime = time.strftime('%H:%M:%S', time.localtime(os.path.getmtime(item)))
            createTimeList.append(ctime)
    os.chdir(fileDir)
    np.savetxt('createTime.csv', createTimeList, delimiter=",", fmt='%s')

def reduce_time_redundancy():
    print("Reducing time redundancy.....", end="", flush=True)
    #scoreList
    #createTimeList
    d = {}
    newDict = {}
    for a, b in zip(createTimeList, scoreList):
        d.setdefault(a,[]).append(b)
    for key in d:
        newDict[key] = sum(d[key])/len(d[key])
    with open("sa_sort_confidences.csv", 'w') as f:
        fieldNames = ['Time', 'AvgConfidence']
        writer = csv.DictWriter(f, fieldnames=fieldNames, lineterminator='\n')
        writer.writeheader()
        data = [dict(zip(fieldNames, [k, v])) for k, v in newDict.items()]
        writer.writerows(data)
        f.close()


##DIRECTORIES

print("Input directory of XMLs and PNGs (Must be together!):")
mainDir = input()
#mainDir = "C:\\Users\\reidn\\Desktop\\T87 1120\\all_png 5 percent"
fileDir = mainDir+ "\\"+"GenFiles"+shortTime
os.mkdir(fileDir)


get_confidence()
print("DONE")
xml_confidences()
print("DONE")
picture_time()
print("DONE")
reduce_time_redundancy()
print("DONE")
