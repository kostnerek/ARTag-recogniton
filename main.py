from PIL import Image
from PIL import ImageFilter
import os 
import pygame.camera 
import cv2 as cv
import numpy as np
import time
import math 
import glob
import pathlib

import parseImage
import shapeDetection as shapeDetect
import similarityCheck as simCheck
import warpPerspective as warp

_PHOTO_ = 'photos/test1.png'
_END_PHOTO_PATH_ = 'photos/endPicture.jpg'
#makes photo using pygame
def makePhoto():
    pygame.camera.init()
    cam = pygame.camera.Camera(0,(640,480))
    cam.start()
    img = cam.get_image()
    pygame.image.save(img,_PHOTO_)

makePhoto()

image = cv.imread(_PHOTO_)

contouredPhoto = parseImage.contourPhoto(image)                 #finding contours on original photo
extractedLinesPhoto = parseImage.extractLines(contouredPhoto)   #extracting contours on black canvas
squaresCoordinates = shapeDetect.detect(extractedLinesPhoto,1)    #marking all squares found in those contours
parsedCoordinates = shapeDetect.getCoords(squaresCoordinates)   #parsing all coordinates 

cropped = image[parsedCoordinates[0]:parsedCoordinates[1],
                parsedCoordinates[2]:parsedCoordinates[3]]      #crops original with parsedCoordinates

cHeight = cropped.shape[0]
cWidth = cropped.shape[1]

warpedPhoto = warp.warp(cropped,squaresCoordinates[0])          #warps photo using square coordinates aquired before
grayscalePhoto = parseImage.grayScaleImage(warpedPhoto,120)         #makes image gray scale - number corresponds to threshold of changing pixel colors 
cv.imwrite(_END_PHOTO_PATH_,grayscalePhoto[0:cHeight, 0:cWidth])   #deletes black box surrounding warped photo

_ARTagCode = simCheck.checkSimilarity(_END_PHOTO_PATH_)         #checks similarity of parsedPhoto with all of template ARTags in .\artags

print(_ARTagCode)








