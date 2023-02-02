# Lesson 11 - Processing Mouse Clicks and Events

import cv2
print(cv2.__version__)

evt=0

def mouseClick(event,xPos,yPos,flags,params):
    global evt
    global pnt
    if event == cv2.EVENT_LBUTTONDOWN:
        print('Mouse Event Was: ',event)
        print('at Position ',xPos,yPos)
        pnt=(xPos,yPos)
        evt = event
    if event == cv2.EVENT_LBUTTONUP:
        print('Mouse Event Was: ',event)
        print('at Position ',xPos,yPos)
        pnt=(xPos,yPos)
        evt=event
    if event == cv2.EVENT_RBUTTONUP:
        print('Right Button Up ',event)
        pnt=(xPos,yPos)
        evt=event

width=640
height=360
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
cv2.namedWindow('my WEBcam')
cv2.setMouseCallback('my WEBcam',mouseClick) # Listener for mouse clicks in specific window and then call a custom function
while True:
    ignore,  frame = cam.read()
    if evt==1 or evt==4:
        cv2.circle(frame,pnt,25,(255,0,0),2)
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        cv2.destroyAllWindows()
        break
cam.release()