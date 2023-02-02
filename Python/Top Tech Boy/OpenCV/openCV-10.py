# Lesson 9 Homework - Understanding Region Of Interest (ROI)

# 1. Take the whole frame and convert to gray scale
# 2. Put a color box back in gray scale
# 3. Move the color box around the area of the larger frame continuously

import cv2
print(cv2.__version__)
width=640
height=360
snipW=120
snipH=60

boxCR=int(height/2)
boxCC=int(width/2)

deltaRow=1
deltaColumn=1

cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
while True:
    ignore,  frame = cam.read()
    frameROI=frame[boxCR-int(snipH/2):boxCR+int(snipH/2),boxCC-int(snipW/2):boxCC+int(snipW/2)]
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)     
    frame=cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)  
    frame[boxCR-int(snipH/2):boxCR+int(snipH/2),boxCC-int(snipW/2):boxCC+int(snipW/2)]=frameROI

    if boxCR-snipH/2<=0 or boxCR+snipH/2>=height:
        deltaRow=deltaRow*(-1)
    if boxCC-snipW/2<=0 or boxCC+snipW/2>=width:
        deltaColumn=deltaColumn*(-1)

    boxCR=boxCR+deltaRow
    boxCC=boxCC+deltaColumn

    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    cv2.imshow('my ROI', frameROI)
    cv2.moveWindow('my ROI',0, 500)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        cv2.destroyAllWindows()
        break
cam.release()