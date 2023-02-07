# Lesson 12 Homework - Understanding the HSV Color Space

# 1. Generate a window that has an HSV rainbow. As you go across the window, the HUE needs to change from 0 to 179
#    and up and down the saturation goes from 0 to 255. Make the value 255
# 2. Generate second window with HUE on rows and value on columns. Set saturation to 255

import cv2
import numpy as np

x=np.zeros([256,720,3],dtype=np.uint8)
for row in range(0,256,1):
    for col in range(0,720,1):
        x[row,col]=(int(col/4),row,255)
x=cv2.cvtColor(x,cv2.COLOR_HSV2BGR)

y=np.zeros([256,720,3],dtype=np.uint8)
for row in range(0,256,1):
    for col in range(0,720,1):
        y[row,col]=(int(col/4),255,row)
y=cv2.cvtColor(y,cv2.COLOR_HSV2BGR)

while True:
    cv2.imshow('my HSV',x)
    cv2.moveWindow('my HSV',0,0)
    cv2.imshow('my HSV2',y)
    cv2.moveWindow('my HSV2',0,300)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
        cv2.destroyAllWindows()

