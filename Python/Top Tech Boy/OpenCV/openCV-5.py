# Lesson 7 - Understanding Pictures and Images as Data Arrays

import cv2
print(cv2.__version__)
import numpy as np

while True:
    frame=np.zeros([250,250,3],dtype=np.uint8)
    frame[:,:]=(255,255,255)
    frame[:83,:83]=(0,0,0)
    frame[:83,166:]=(0,0,0)
    frame[83:166,83:166]=(0,0,0)
    frame[166:,:83]=(0,0,0)
    frame[166:,166:]=(0,0,0)
    cv2.imshow('My Window', frame)
    if cv2.waitKey(1) & 0xff==ord('q'):
        break