import cv2 
import numpy as np


#outlines sharp countours on photo 
def contourPhoto(image, mode=0):
    cv2.waitKey(0) 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    edged = cv2.Canny(gray, 30, 200) 
    cv2.waitKey(0) 
    contours, hierarchy = cv2.findContours(edged,  
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    
    cv2.drawContours(image, contours, -1, (0, 0, 255), 1) 
    if(mode==1):
        cv2.imshow('Contours', image) 
    cv2.waitKey(0) 
    cv2.destroyAllWindows() 

#highlines all coutours on photo by changing everything other than them to black
def extractLines(image, mode=0):
    lower_range = np.array([0,0,255])  # Set the Lower range value of color in BGR
    upper_range = np.array([0,0,255])   # Set the Upper range value of color in BGR
    mask = cv2.inRange(image,lower_range,upper_range) # Create a mask with range
    result = cv2.bitwise_and(image,image,mask = mask)  # Performing bitwise and operation with mask in img variable
    if(mode==1):
        cv2.imshow('Image1',result) # Image after bitwise operation
    cv2.waitKey(0)
    cv2.destroyWindow('Image1')
    cv2.imwrite('extractedLines.jpg',result)