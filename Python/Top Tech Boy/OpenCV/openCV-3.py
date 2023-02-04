# Lesson 6 - Faster launch of webcam and smoother video

import cv2
print(cv2.__version__)
width = 640
height = 360
cam=cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
while True:
    ignore, frame = cam.read() # this function returns two parameters, you can just ignore the first one    
    cv2.imshow('my WEBcam', frame) # define a name and then what to show
    cv2.moveWindow('my WEBcam', 0,0)
    if cv2.waitKey(1) & 0xff == ord('q'): # wait 1 millisecond to see if user has pressed the q button for quit
        cv2.destroyAllWindows()
        break
cam.release()
