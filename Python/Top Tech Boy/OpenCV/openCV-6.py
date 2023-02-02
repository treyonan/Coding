# Lesson 7 Homework - Understanding Pictures and Images as Data Arrays

import cv2
print(cv2.__version__)
import numpy as np

boardSize = int(input('What Size is your Board, Boss?'))
numSquares = int(input('And Sir, How Many Squares? '))
squareSize = int(boardSize/numSquares)

darkColor=(0,0,0)
lightColor=(0,0,255)
nowColor=darkColor

while True:
    x=np.zeros([boardSize,boardSize,3],dtype=np.uint8)

    for row in range(0,numSquares):
        for column in range(0,numSquares):
            x[squareSize*row:squareSize*(row+1),squareSize*column:squareSize*(column+1)]=nowColor
            if nowColor==darkColor:
                nowColor=lightColor
            else:
                nowColor=darkColor
        
        if nowColor==darkColor:
            nowColor=lightColor
        else:
            nowColor=darkColor

    cv2.imshow('My Checkerboard', x)
    if cv2.waitKey(1) & 0xff== ord('q'):
        break
