# Lesson 15 Homework: Face Detection using OpenCV

# 1. print FPS with face detection
# 2. add eye detection and put red rectangles around each eye

import cv2
print(cv2.__version__)
import time
width=640
height=360

tLast=time.time()
time.sleep(.1)
fpsFILT=30
myFont=cv2.FONT_HERSHEY_COMPLEX
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

faceCascade=cv2.CascadeClassifier(r'C:\Users\trey_\OneDrive\Projects\Coding\Python\Top Tech Boy\OpenCV\haar\haarcascade_frontalface_default.xml')
eyeCascade=cv2.CascadeClassifier(r'C:\Users\trey_\OneDrive\Projects\Coding\Python\Top Tech Boy\OpenCV\haar\haarcascade_eye.xml')

while True:
    dT=time.time()-tLast    
    fps=1/dT
    fpsFILT=fpsFILT*.97+fps*.03 # This is a low pass filter to smooth fps rate reading. Confidence in old number (fptFILT) + confidence in instantaneous number (fps)
    tLast=time.time()
    ignore,  frame = cam.read()
    frameGray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(frameGray,1.3,5) # 1.3 is confidence level. faces will return an array of arrays for each face. 
                                                        # each array will contain 4 numbers. x and y of upper left corner of rectangle, width and height of rectangle

    eyes=eyeCascade.detectMultiScale(frameGray,1.3,5)

    for face in faces:
        x,y,w,h=face        
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3) # draw rectangle on original frame with coordinates from frace
        frameROI=frame[y:y+h,x:x+w]
        frameROIGray=cv2.cvtColor(frameROI,cv2.COLOR_BGR2GRAY)
        eyes=eyeCascade.detectMultiScale(frameROIGray)

        for eye in eyes:
            x2,y2,w2,h2=eye
            cv2.rectangle(frame[y:y+h,x:x+w],(x2,y2),(x2+w2,y2+h2),(0,0,255),3)

    cv2.putText(frame,str(int(fpsFILT))+' fps',(70,150),myFont,2,(255,0,0),2)
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        cv2.destroyAllWindows()
        break
cam.release()

