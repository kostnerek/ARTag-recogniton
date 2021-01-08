from PIL import Image
from PIL import ImageFilter

import pygame.camera 
import cv2 
import numpy as np
import shapeDetection as detect
import parseImage

import os 


_PHOTO_ = 'photo.jpg'

#makes photo using pygame
def makePhoto():
    pygame.camera.init()
    cam = pygame.camera.Camera(0,(640,480))
    cam.start()
    img = cam.get_image()
    pygame.image.save(img,_PHOTO_)

image = cv2.imread(_PHOTO_)

for x in range(1):
    makePhoto()
    parseImage.contourPhoto(image)
    parseImage.extractLines(image)

    squares=detect.detect('extractedLines.jpg')
    coords = detect.getCoords(squares)
    print(squares)
    image = cv2.imread(_PHOTO_)
    cropped = image[coords[0]:coords[1],coords[2]:coords[3]]
    cv2.imwrite("result.png",cropped)



