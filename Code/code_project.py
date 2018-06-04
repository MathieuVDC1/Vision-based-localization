# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 15:46:35 2018

@author: Mathieu
"""


import cv2
import numpy  as np
np.set_printoptions(threshold=np.nan)
import math
import sys
import os.path
import time
import copy
   

def getDataSpecificFrame(inputFolder,frameNumber,amountOfLines):
    frame = inputFolder + "\\frame" + str(frameNumber) +  ".png"
    image = cv2.imread(frame,1)
    lines = detectXBestLines(amountOfLines,image)
    return lines, image
    

def overlayEdgesOnImage(imageOrg,edgeImage):
    for i in range(imageOrg.shape[1]):
        for j in range(imageOrg.shape[0]):
            if(edgeImage[j,i] == 255):
                imageOrg[j,i] = [0,0,255]
            
    return imageOrg

def removeDuplicateLines(lines):
    amountOfLines = np.size(lines)/2
    for i in range(0,amountOfLines):  
        r = lines[0:amountOfLines,0,0]                              
        rr = copy.copy(r)
        rr[i+1:amountOfLines] = np.abs(r[i+1:amountOfLines] - r[i])
        rr[rr<50] = 0.0
        rr[rr>=50] = 1.0
        lines[0:amountOfLines,0,0] *= rr
        lines[0:amountOfLines,0,1] *= rr       
    linesNew = np.zeros([np.nonzero(lines[0:amountOfLines,0,0])[0].size,2])
    k = 0
    for i in range(0,np.size(lines)/2):
        if(lines[i].any() != 0):
            linesNew[k] = lines[i]
            k+=1
    return linesNew

def drawLines(image,lines):
    punten = np.array([[[0,0],[0,0]],[[0,0],[0,0]]])
    for i in range(0,np.size(lines)/2):                                
        rho = lines[i,0]                 
        theta = lines[i,1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        punten[0,0,0] = np.round(x0 + 10000*(-b))
        punten[0,0,1] = np.round(y0 + 10000*(a))
        punten[1,1,0] = np.round(x0 - 10000*(-b))
        punten[1,1,1] = np.round(y0 - 10000*(a))
        cv2.line(image,(punten[0,0,0],punten[0,0,1]),(punten[1,1,0],punten[1,1,1]),(255,0,0),1)
    
    cv2.imshow('lines',image)  
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return image
    

def detectXBestLines(x,image):
    BestLines = np.zeros([x,2])
    imageBlur = cv2.GaussianBlur(image,(11,11),2.5,2.5)
    edge = cv2.Canny(imageBlur,50,100)
    for i in range(0,edge.shape[1]):
        r = edge[0:edge.shape[0],i]
        nonzero = np.nonzero(r)
        firstIndex = 0
        if(nonzero[0].size == 0):
            firstIndex = 0
        else:
            firstIndex = nonzero[0][0]
        edge[firstIndex+1:edge.shape[1],i] = 0
    lines = cv2.HoughLines(edge,1,math.pi/180,20)
    lines = removeDuplicateLines(lines)
    for i in range(0,min(x,np.size(lines)/2-1)):
        BestLines[i] = lines[i]
    return BestLines
    
def determineMatch(lines1,lines2,amountOfLines):
    sum = 0
    for i in range(0,amountOfLines-1):
        r = copy.copy(lines2)
        r[0:amountOfLines,0] -= lines1[i,0]
        r[0:amountOfLines,1] -= lines1[i,1]
        sum += np.min(np.abs(r[0:amountOfLines,0]+100*r[0:amountOfLines,1]))
    return sum
            
    
def determineAndWriteTrainingFramesData(inputFolder, outputFile,amountOfLines,amount = 0,startFrame = 0,count = 30):
    file = open(outputFile,"w")
    if amount == 0:
        frameCount = len(os.listdir(inputFolder))
    else:
        frameCount = amount
    for i in range(0,frameCount-1):
        frameNumber = i*30+30*startFrame
        frame = inputFolder + "\\frame" + str(frameNumber) +  ".png"
        image = cv2.imread(frame,1)
        lines = detectXBestLines(amountOfLines,image)
        file.write(str(frameNumber)+ "\n")
        for j in range(0,amountOfLines):
            file.write(str(lines[j,0])+ " " +str(lines[j,1])+ "\n")
        file.write("\n")
        print i
        
def readTrainingFramesData(dataFile,amountOfFrames,amountOfLines):  
    file = open(dataFile,"r")
    data = np.empty([amountOfFrames,amountOfLines+1,2])
    for i in range(0,amountOfFrames-1):
        data[i,0,0] = i
        data[i,0,1] = float(file.readline())
        for j in range(1,amountOfLines+1):
            str = file.readline()
            data[i,j,0] = float(str.split()[0])
            data[i,j,1] = float(str.split()[1])
        file.readline()
        
    return data

def getBestMatch(data,startFrame,stopFrame,image,amountOfLines):   #Determines best match of image and dataset 
    bestMatch = 10000                                #between startFrame & stopFrame
    bestFrame = 0                                
    amountOfFrames = stopFrame-startFrame
    lines = detectXBestLines(amountOfLines,image)
    for i in range(startFrame,stopFrame):
        match = determineMatch(data[i,1:amountOfLines],lines,amountOfLines)
        if(match < bestMatch):
            bestMatch = match
            bestFrame = data[i,0,1]
    drawLines(image,lines)
    return bestFrame,bestMatch
    

    
determineAndWriteTrainingFramesData("D:\\School\\2017 - 2018\\Semester 2\\Computervisie\\Project\\Frames1",
                                    "dataTrainingFrames2.txt",3,amount = 20)
    





'''
data = readTrainingFramesData("dataTrainingFrames3.txt",847,3)
bestmatch = 10000
bestframe = 1
comparedFrame = 0
for i in range(112,119):
    image = cv2.imread("D:\\School\\2017 - 2018\\Semester 2\\Computervisie\\Project\\Frames2_15fps\\frame0" + str(i) + ".png",1)
    bestFrame, bestMatch =  getBestMatch(data,0,847,image,3)
    if(bestMatch < bestmatch):
        bestmatch = bestMatch
        bestframe = bestFrame
        comparedframe = i
print comparedframe, int(bestframe),bestmatch

'''
'''
bestmatch = 10000
bestframe = 1
comparedFrame = 0
for i in range(135,142):
    image = cv2.imread("D:\\School\\2017 - 2018\\Semester 2\\Computervisie\\Project\\Frames2_15fps\\frame0" + str(i) + ".png",1)
    bestFrame, bestMatch =  getBestMatch(data,0,847,image,3)
    if(bestMatch < bestmatch):
        bestmatch = bestMatch
        bestframe = bestFrame
        comparedframe = i
print comparedframe, int(bestframe),bestmatch
'''

'''
data = readTrainingFramesData("dataTrainingFrames3.txt",847,3)
bestmatch = 10000
bestframe = 1
comparedFrame = 0
for i in range(184,192):
    image = cv2.imread("D:\\School\\2017 - 2018\\Semester 2\\Computervisie\\Project\\Frames2_15fps\\frame0" + str(i) + ".png",1)
    bestFrame, bestMatch =  getBestMatch(data,52,82,image,3)
    if(bestMatch < bestmatch):
        bestmatch = bestMatch
        bestframe = bestFrame
        comparedframe = i
print comparedframe, int(bestframe),bestmatch
'''

