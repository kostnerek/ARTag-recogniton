from arrayLib import Array
import cv2 as cv
import numpy as np
from PIL import Image
class ARTag:
    def __init__(self,size,image):
        self.tag = Array(size,size,1)
        #self.tag.printArray(1,1)
        self.size  = size
        self.imgName = image
        self.image = cv.imread(image)
        self.cutOnParts()

    def cutOnParts(self):
        self.width = self.image.shape[0]
        self.height = self.image.shape[1]
        self.partWidth  = int(self.width/self.size)
        self.partHeight = int(self.height/self.size)

        for x in range(self.size):
            start_point = (self.partWidth*x,0)
            end_point = (self.partWidth*x,self.height)
            self.image = cv.line(self.image, start_point, end_point, (0,255,0), 1) 
        for x in range(self.size):
            start_point = (0,self.partHeight*x)
            end_point = (self.width,self.partWidth*x)
            self.image = cv.line(self.image, start_point, end_point, (0,255,0), 1) 

        for y in range(self.size):
            for x in range(self.size):
                #coords=[self.partHeight*x,self.partHeight*x,self.partHeight,self.partWidth*x+self.partWidth]
                left = self.partWidth*x
                upper = self.partHeight*y
                right = left+self.partWidth
                lower = upper+self.partHeight

                coords=[left, upper, right, lower]
                #print(x,y)
                mark = self.getPixel(coords)
                if(mark==1):
                    self.tag.modify(y,x,1)
                else:
                    self.tag.modify(y,x,0)
                
       

    def getPixel(self,coords):
        im = Image.open(self.imgName)
        im = im.crop((coords[0],coords[1],coords[2],coords[3]))
        imconv = im.convert("RGB")
        w=0
        b=0
        for y in range(self.partHeight):
            for x in range(self.partWidth):
                if(imconv.getpixel((x,y))[0]==0):
                    b+=1
                else:
                    w+=1
        if(w<b):
            return 1
        else:
            return 0

    def showImage(self):
        cv.imshow('squares', self.image)
        ch = cv.waitKey()
    
