# Lesson 16 Homework - Face Recognition with OpenCV

# 1. Perform live tracking with family members


import cv2
import face_recognition as FR
font=cv2.FONT_HERSHEY_SIMPLEX
donFace=FR.load_image_file(r'C:/Users/trey_/OneDrive/Projects/Coding/Python/Top Tech Boy/OpenCV/demoImages/known/Donald Trump.jpg')
faceLoc=FR.face_locations(donFace)[0] # Will return 4 numbers in a tuple inside of an array. 1st number is top, 2nd number is right, 3rd number is bottom, 4th number is left
donFaceEncode=FR.face_encodings(donFace)[0]

nancyFace=FR.load_image_file(r'C:/Users/trey_/OneDrive/Projects/Coding/Python/Top Tech Boy/OpenCV/demoImages/known/Nancy Pelosi.jpg')
faceLoc=FR.face_locations(nancyFace)[0]
nancyFaceEncode=FR.face_encodings(nancyFace)[0]

mikeFace=FR.load_image_file(r'C:/Users/trey_/OneDrive/Projects/Coding/Python/Top Tech Boy/OpenCV/demoImages/known/Mike Pence.jpg')
faceLoc=FR.face_locations(mikeFace)[0]
mikeFaceEncode=FR.face_encodings(mikeFace)[0]

knownEncodings=[donFaceEncode,nancyFaceEncode,mikeFaceEncode]
names=['Donald Trump', 'Nancy Pelosi','Mike Pence']

unknownFace=FR.load_image_file(r'C:/Users/trey_/OneDrive/Projects/Coding/Python/Top Tech Boy/OpenCV/demoImages/unknown/u1.jpg')
unknownFaceBGR=cv2.cvtColor(unknownFace,cv2.COLOR_RGB2BGR)
faceLocations=FR.face_locations(unknownFace)
unknownEncodings=FR.face_encodings(unknownFace,faceLocations)

for faceLocation,unknownEncoding in zip(faceLocations,unknownEncodings):
    top,right,bottom,left=faceLocation
    print(faceLocation)
    cv2.rectangle(unknownFaceBGR,(left,top),(right,bottom),(255,0,0),3)
    name='Unknown Person'
    matches=FR.compare_faces(knownEncodings,unknownEncoding)
    print(matches)
    if True in matches:
        matchIndex=matches.index(True)
        print(matchIndex)
        print(names[matchIndex])
        name=names[matchIndex]
    cv2.putText(unknownFaceBGR,name,(left,top),font,.75,(0,0,255),2)
cv2.imshow('My Faces',unknownFaceBGR)
#top,right,bottom,left=faceLoc
#cv2.rectangle(donFace,(left,top),(right,bottom),(255,0,0),3)
#donFaceBGR=cv2.cvtColor(donFace,cv2.COLOR_RGB2BGR)
#cv2.imshow('My Window', donFaceBGR)
cv2.waitKey(5000)