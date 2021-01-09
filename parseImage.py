import cv2 
import numpy as np
from PIL import Image 
from ar_markers import detect_markers

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


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def hardBWconvert(name,thresh=170):
    img = Image.open(name)
    fn = lambda x : 255 if x > thresh else 0
    r = img.convert('L').point(fn, mode='1')
    r.save(name)

def parseARTag(image, thresh=200, mode=0):

    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    image = cv2.filter2D(image, -1, kernel)

    """ cv2.imshow('Image1',image)
    cv2.waitKey(0)
    cv2.destroyWindow('Image1')
    cv2.imwrite('sharpened.jpg',image) """


    lower_range = np.array([thresh,thresh,thresh])  # Set the Lower range value of color in BGR
    upper_range = np.array([255,255,255])   # Set the Upper range value of color in BGR
    mask = cv2.inRange(image,lower_range,upper_range) # Create a mask with range
    result = cv2.bitwise_and(image,image,mask = mask)  # Performing bitwise and operation with mask in img variable

    cv2.imwrite('result.jpg',result)
    hardBWconvert("result.jpg",thresh)

