from arrayLib import Array
import cv2 as cv
import numpy as np
from PIL import Image
import parseImage 

class ARTag:
    def __init__(self,size,image, saveParts=False):
        self.saveParts = saveParts
        self.count=0
        self.tag = Array(size,size,1)
        #self.tag.printArray(1,1)
        self.size  = size
        self.imgName = image
        self.image = self.getColoredSides()
        cv.imwrite('photos/endPicture.jpg',self.image)
        #self.cutOnParts()
        cv.imwrite('photos/endPictureWithLines.jpg',self.image)

    def getColoredSides(self):
        self.image = cv.imread(self.imgName)
        self.width = self.image.shape[0]
        self.height = self.image.shape[1]
        self.partWidth  = int(self.width/self.size)
        self.partHeight = int(self.height/self.size)
        #return cv.imread(self.imgName)
        return parseImage.colorSides(self.image,(self.width,self.height), (self.partWidth, self.partHeight))

    def cutOnParts(self):
        
        for x in range(self.size):
            start_point = (self.partWidth*x,0)
            end_point = (self.partWidth*x,self.height)
            self.image = cv.line(self.image, start_point, end_point, (0,255,0), 1) 
        for x in range(self.size):
            start_point = (0,self.partHeight*x)
            end_point = (self.width,self.partWidth*x)
            self.image = cv.line(self.image, start_point, end_point, (0,255,0), 1) 

        self.image = cv.line(self.image,(0,self.width), (self.height,self.width), (0,255,0), 2) 
        self.image = cv.line(self.image,(self.width,0), (self.height,self.width), (0,255,0), 2) 
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
        #coords=[yMin,yMax,xMin,xMax]
        im = Image.open("photos/endPicture.jpg")
        im = im.crop((coords[0],coords[1],coords[2],coords[3]))
        ''' fn = lambda x : 255 if x > 128 else 0
        imconv = im.convert('L').point(fn, mode='1') '''
        imconv = im.convert("RGB")
        w=0
        b=0

        for y in range(self.partHeight):
            for x in range(self.partWidth):
                if(imconv.getpixel((x,y))>(128,128,128)):
                    w+=1
                else:
                    b+=1
        #shows cut parts
        
        self.count+=1
        pxCount = self.partHeight*self.partWidth
        
        if(self.saveParts==True):
            part = 'cutParts/part'
            part+=str(self.count)
            part+='w'
            part+=str(w)
            part+='b'
            part+=str(b)
            part+='.jpg'
            im.save(part)
            print(self.count,' w:',w,"b:",b,' pxCount: ',pxCount)
        
        if(w<b):#if whites are less than black+10% of part px count 
            return 1
        else:
            return 0

    def showImage(self):
        cv.imshow('squares', self.image)
        ch = cv.waitKey()
    
