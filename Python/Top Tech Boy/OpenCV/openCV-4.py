# Lesson 6 - Faster launch of webcam and smoother video

import cv2
print(cv2.__version__)

rows = int(input('Boss, How Many Rows do You Want? '))
columns = int(input('And How Many Columns'))

width = 640
height = 360
cam=cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
while True:
    ignore, frame = cam.read() # this function returns two parameters, you can just ignore the first one    
    frame = cv2.resize(frame,(int(width/columns), int(height/columns)))
    for i in range(0, rows):
        for j in range(0, columns):
            windName = 'Window'+str(i)+' x '+str(j)
            cv2.imshow(windName, frame) # define a name and then what to show
            cv2.moveWindow(windName, int(width/columns)*j, int(height/columns+30)*i)
    if cv2.waitKey(1) & 0xff == ord('q'): # wait 1 millisecond to see if user has pressed the q button for quit
        cv2.destroyAllWindows()
        break
cam.release()
