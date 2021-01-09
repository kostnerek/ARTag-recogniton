from PIL import Image
from PIL import ImageFilter
import os 
import pygame.camera 
import cv2 
import numpy as np

import shapeDetection as detect
import parseImage
from getDataFromTag import ARTag


_PHOTO_ = 'photo.jpg'


#makes photo using pygame
def makePhoto():
    pygame.camera.init()
    cam = pygame.camera.Camera(0,(640,480))
    cam.start()
    img = cam.get_image()
    pygame.image.save(img,_PHOTO_)

image = cv2.imread(_PHOTO_)

def determineCoords(squares):
    xCoords=[]
    yCoords=[]
    for x in range(len(squares)):
        for y in range(len(squares[x])):
            for z in range(len(squares[x][y])):
                if(z==0):
                    xCoords.append(squares[x][y][z])
                else:
                    yCoords.append(squares[x][y][z])


for x in range(2):
    makePhoto()
    parseImage.contourPhoto(image)
    parseImage.extractLines(image)

    squares=detect.detect('extractedLines.jpg')
    coords = detect.getCoords(squares)
    
    image = cv2.imread(_PHOTO_)
    cropped = image[coords[0]:coords[1],coords[2]:coords[3]]
    

crd = squares[0]


tRX = crd[1][0]
tRY = crd[1][1]
tLX = crd[0][0]
tLY = crd[0][1]

#print(crd[0],crd[1])
wsp_kier = (tLY - tRY) / (tLX - tRX)
wsp_kier=0
print('wsp kier:',wsp_kier)

cv2.imwrite("cropped.jpg",parseImage.rotate_image(cropped, -wsp_kier))

parseImage.parseARTag(parseImage.rotate_image(cropped, -wsp_kier),130)


#size of inside + 4 for outline 
tag = ARTag(10,"result.jpg")
tag.tag.printReplace(1,1,1,'X',0,' ')
tag.showImage()