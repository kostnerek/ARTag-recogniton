import cv2 
import numpy as np
from PIL import Image 
from ar_markers import detect_markers

_END_PHOTO_PATH_ = 'photos/endPicture.jpg'


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
    return image

#highlines all coutours on photo by changing everything other than them to black
def extractLines(image, mode=0, savePhoto=False):
    lower_range = np.array([0,0,255])  # Set the Lower range value of color in BGR
    upper_range = np.array([0,0,255])   # Set the Upper range value of color in BGR
    mask = cv2.inRange(image,lower_range,upper_range) # Create a mask with range
    result = cv2.bitwise_and(image,image,mask = mask)  # Performing bitwise and operation with mask in img variable
    if(mode==1):
        cv2.imshow('Image1',result) # Image after bitwise operation
        cv2.waitKey(0)
        cv2.destroyWindow('Image1')
    if(savePhoto==True):
        cv2.imwrite('photos/extractedLines.jpg',result)
    return result 

#rotates image 
def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

#convert to strict black and white 
def hardBWconvert(name,thresh=170):
    img = Image.open(name)
    fn = lambda x : 255 if x > thresh else 0
    r = img.convert('L').point(fn, mode='1')
    r.save(name)

#makes picture grayscale? i think so...
def grayScaleImage(image, thresh=200,saveImage=False):

    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    image = cv2.filter2D(image, -1, kernel)

    lower_range = np.array([thresh,thresh,thresh])  # Set the Lower range value of color in BGR
    upper_range = np.array([255,255,255])   # Set the Upper range value of color in BGR
    mask = cv2.inRange(image,lower_range,upper_range) # Create a mask with range
    result = cv2.bitwise_and(image,image,mask = mask)  # Performing bitwise and operation with mask in img variable
    if(saveImage==True):
        cv2.imwrite('photos/grayScale.jpg',result)
    hardBWconvert(_END_PHOTO_PATH_,thresh)#makes mostly black pxs black and so on
    return result
    

""" def colorSides(image,dimentions,part_dimentions):
    #w,h
    pWidth = part_dimentions[0]
    pHeight = part_dimentions[1]
    
    width = dimentions[0]
    height = dimentions[1]

    black = (0,0,0)

    cv2.rectangle(image,(0,0),(width,pHeight*2),black,-1)
    cv2.rectangle(image,(0,0),(pHeight*2,height),black,-1)
    cv2.rectangle(image,(width-pWidth*2,0),(width+2,height),black,-1)
    cv2.rectangle(image,(0,height-pHeight*2),(width,height),black,-1)

    return image """

