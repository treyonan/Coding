# Lesson 15 Homework: Face Detection using OpenCV

# 1. print FPS with face detection
# 2. add eye detection and put red rectangles around each eye

import cv2
print(cv2.__version__)
width=640
height=360
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

faceCascade=cv2.CascadeClassifier(r'C:\Users\trey_\OneDrive\Projects\Coding\Python\Top Tech Boy\OpenCV\haar\haarcascade_frontalface_default.xml')

while True:
    ignore,  frame = cam.read()
    frameGray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(frameGray,1.3,5) # 1.3 is confidence level. faces will return an array of arrays for each face. 
                                                        # each array will contain 4 numbers. x and y of upper left corner of rectangle, width and height of rectangle
    for face in faces:
        x,y,w,h=face
        print(x,y,w,h)
        cv2.rectangle(frame,(x,y),(x+width,y+height),(255,0,0),3) # draw rectangle on original frame with coordinates from frace

    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        cv2.destroyAllWindows()
        break
cam.release()