# Lesson 17 - Walk through your file system with os.walk

import os
import cv2
import face_recognition as FR
print(cv2.__version__)
imageDir=r'C:\Users\trey_\OneDrive\Projects\Coding\Python\Top Tech Boy\OpenCV\demoImages/known'
for root,dirs,files in os.walk(imageDir):
    print('my Working Folder (root): ', root)
    print('dirs in root: ', dirs)
    print('My Files in root: ', files)
    for file in files:
        print('Your Guy Is: ', file)
        fullFilePath=os.path.join(root,file)
        print(fullFilePath)
        name=os.path.splitext(file)[0]
        print(name)
        myPicture=FR.load_image_file(fullFilePath)
        myPicture=cv2.cvtColor(myPicture,cv2.COLOR_RGB2BGR)
        cv2.imshow(name,myPicture)
        cv2.moveWindow(name,0,0)
        cv2.waitKey(2500)
        cv2.destroyAllWindows()

