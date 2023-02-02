# Lesson 5

import cv2
print(cv2.__version__)
cam=cv2.VideoCapture(0)
while True:
    ignore, frame = cam.read() # this function returns two parameters, you can just ignore the first one
    grayFrame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert from color frame to gray
    cv2.imshow('my WEBcam', grayFrame) # define a name and then what to show
    cv2.moveWindow('my WEBcam', 0,0)
    if cv2.waitKey(1) & 0xff == ord('q'): # wait 1 millisecond to see if user has pressed the q button for quit
        cv2.destroyAllWindows()
        break
cam.release()
