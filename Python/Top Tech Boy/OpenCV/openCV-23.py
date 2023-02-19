import cv2
import face_recognition as FR
font=cv2.FONT_HERSHEY_SIMPLEX
donFace=FR.load_image_file(r'C:/Users/trey_/OneDrive/Projects/Coding/Python/Top Tech Boy/OpenCV\demoImages/known\Donald Trump.jpg')
faceLoc=FR.face_locations(donFace) # Will return 4 numbers in a tuple inside of an array. 1st number is top, 2nd number is right, 3rd number is bottom, 4th number is left
print(faceLoc)