# Lesson 13 Homework - Tracking an Object Based on Color in OpenCV

# 1. Track on two different color objects
# 2. Track red by using two different color ranges since it straddles zero. Will need two sets of track bars for hue

import cv2
import numpy as np
print(cv2.__version__)

def onTrack1(val):
    global hueLow
    hueLow=val
    print('Hue Low',hueLow)

def onTrack2(val):
    global hueHigh
    hueHigh=val
    print('Hue High',hueHigh)

def onTrack3(val):
    global satLow
    satLow=val
    print('Sat Low',satLow)

def onTrack4(val):
    global satHigh
    satHigh=val
    print('Sat High',satHigh)

def onTrack5(val):
    global valLow
    valLow=val
    print('Val Low',valLow)

def onTrack6(val):
    global valHigh
    valHigh=val
    print('Val High',valHigh)

def onTrack7(val):
    global hueLow2
    hueLow2=val
    print('Hue Low 2',hueLow2)

def onTrack8(val):
    global hueHigh2
    hueHigh2=val
    print('Hue High 2',hueHigh2)

width=640
height=360
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

cv2.namedWindow('myTracker',cv2.WINDOW_NORMAL)
cv2.resizeWindow('myTracker',350,350)
cv2.moveWindow('myTracker',width,0)

hueLow=10
hueHigh=20
satLow=10
satHigh=250
valLow=10
valHigh=250

cv2.createTrackbar('Hue Low','myTracker',10,179,onTrack1)
cv2.createTrackbar('Hue High','myTracker',20,179,onTrack2)
cv2.createTrackbar('Hue Low 2','myTracker',10,179,onTrack7)
cv2.createTrackbar('Hue High 2','myTracker',20,179,onTrack8)
cv2.createTrackbar('Sat Low','myTracker',10,255,onTrack3)
cv2.createTrackbar('Sat High','myTracker',250,255,onTrack4)
cv2.createTrackbar('Val Low','myTracker',10,255,onTrack5)
cv2.createTrackbar('Val High','myTracker',250,255,onTrack6)


while True:
    ignore,  frame = cam.read()
    frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lowerBound=np.array([hueLow,satLow,valLow])
    upperBound=np.array([hueHigh,satHigh,valHigh])

    lowerBound2=np.array([hueLow2,satLow,valLow])
    upperBound2=np.array([hueHigh2,satHigh,valHigh])

    myMask=cv2.inRange(frameHSV,lowerBound,upperBound)
    myMask2=cv2.inRange(frameHSV,lowerBound2,upperBound2)

    #myMaskComp=myMask | myMask2
    myMaskComp=cv2.add(myMask,myMask2)

    #myMask=cv2.bitwise_not(myMask)
    myObject=cv2.bitwise_and(frame,frame,mask=myMaskComp)
    myObjectSmall=cv2.resize(myObject,(int(width/2),int(height/2)))
    cv2.imshow('My Object', myObjectSmall) 
    cv2.moveWindow('My Object', int(width/2),int(height)) 
    myMaskSmall=cv2.resize(myMask,(int(width/2),int(height/2)))
    cv2.imshow('My Mask', myMaskSmall)
    cv2.moveWindow('My Mask',0,height)

    myMaskSmall2=cv2.resize(myMask2,(int(width/2),int(height/2)))
    cv2.imshow('My Mask 2', myMaskSmall2)
    cv2.moveWindow('My Mask 2',0,height+int(height/2))

    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        cv2.destroyAllWindows()
        break
cam.release()