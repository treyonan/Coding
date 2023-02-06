# Lesson 11 Homework - Creating and Using Trackbars

# 1. Create a trackbar where the trackbar will define the image size. Use 16:9 ratio by changing cam.set width and height
# 2. Create another trackbar to move the image in two directions

import cv2
print(cv2.__version__)

def myCallBack1(val): 
    myWidth=val
    height=int((9/16)*myWidth)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,myWidth)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)     
    
def myCallBack2(val):
    global xPos    
    xPos=val
def myCallBack3(val):
    global yPos    
    yPos=val

myWidth=1280
height=int((9/16)*myWidth)
xPos=0
yPos=0

cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,myWidth)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)   
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
cv2.namedWindow('myTrackbars')
cv2.resizeWindow('myTrackbars',400,200)
cv2.moveWindow('myTrackbars',1400,0)
cv2.createTrackbar('myWidth','myTrackbars',myWidth,1920,myCallBack1)
cv2.createTrackbar('xPos','myTrackbars',xPos,1080,myCallBack2)
cv2.createTrackbar('yPos','myTrackbars',yPos,1080,myCallBack3)

while True:
    ignore,  frame = cam.read()    
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',xPos,yPos)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        cv2.destroyAllWindows()
        break
cam.release()