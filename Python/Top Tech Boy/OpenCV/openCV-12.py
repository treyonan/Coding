# Lesson 10 Homework - Processing Mouse Clicks and Events

# 1. Create ROI using the mouse
#     Left mouse button down is upper left and left mouse button up is lower right
#     Show ROI off to the side
# 2. Right mouse click will destroy the ROI window

import cv2
print(cv2.__version__)

evt=4

def mouseClick(event,xPos,yPos,flags,params):
    global evt
    global upperLeftpnt
    global lowerRightpnt
    if event == cv2.EVENT_LBUTTONDOWN:
        print('Mouse Event Was: ',event)
        print('at Position ',xPos,yPos)
        upperLeftpnt=(xPos,yPos)
        evt = event
    if event == cv2.EVENT_LBUTTONUP:
        print('Mouse Event Was: ',event)
        print('at Position ',xPos,yPos)
        lowerRightpnt=(xPos,yPos)
        evt=event
    if event == cv2.EVENT_RBUTTONUP:
        print('Right Button Up ',event)        
        evt=event

width=640
height=360
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
cv2.namedWindow('my WEBcam')
cv2.setMouseCallback('my WEBcam',mouseClick)
while True:
    ignore,  frame = cam.read()

    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    
    if evt==4:   
        frameROI=frame[150:210,250:390]           
        cv2.imshow('my ROI', frameROI)
        cv2.moveWindow('my ROI',650,0)
    else:
        cv2.destroyWindow('my ROI')
       
    
    if cv2.waitKey(1) & 0xff ==ord('q'):
        cv2.destroyAllWindows()
        break
cam.release()