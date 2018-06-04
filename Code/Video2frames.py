# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 12:19:30 2018

@author: laven
"""

import cv2

ret  = True
nr = 1
capture = cv2.VideoCapture('2018_02_28_heen.mp4')
ret,frame = capture.read()
print(ret)

while(ret):
    if(nr == 1):
        cv2.imwrite('frames/frame' + str(nr) + '.png', frame)
    
    if(nr%30 == 0):
        cv2.imwrite('frames/frame' + str(nr) + '.png', frame)
        
    ret,frame = capture.read()
    nr += 1