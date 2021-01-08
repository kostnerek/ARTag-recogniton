from __future__ import print_function
import sys
PY3 = sys.version_info[0] == 3

if PY3:
    xrange = range

import numpy as np
import cv2 as cv


def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    img = cv.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv.split(img):
        for thrs in xrange(0, 255, 26):
            if thrs == 0:
                bin = cv.Canny(gray, 0, 50, apertureSize=5)
                bin = cv.dilate(bin, None)
            else:
                _retval, bin = cv.threshold(gray, thrs, 255, cv.THRESH_BINARY)
            contours, _hierarchy = cv.findContours(bin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv.arcLength(cnt, True)
                cnt = cv.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv.contourArea(cnt) > 1000 and cv.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares

#parses coords of squares on photo
#returns max&min x&y values to determine crop coordinates 
def getCoords(squares):
    """ 
    x=sq num
    y=sq coord num
    x={0=x,1=y}
    """
    xCoords=[]
    yCoords=[]
    for x in range(len(squares)):
        for y in range(len(squares[x])):
            for z in range(len(squares[x][y])):
                if(z==0):
                    xCoords.append(squares[x][y][z])
                else:
                    yCoords.append(squares[x][y][z])
    
    xMax = np.max(xCoords)          
    xMin = np.min(xCoords)  
    yMax = np.max(yCoords)          
    yMin = np.min(yCoords)   
    coords=[yMin,yMax,xMin,xMax]
    return coords 

def detect(_PHOTO_, mode=0):
    from glob import glob
    for fn in glob(_PHOTO_):
        img = cv.imread(fn)
        squares = find_squares(img)
        cv.drawContours( img, squares, -1, (0, 255, 0), 1 )
        if(mode==1):
            cv.imshow('squares', img)
        #cv.imwrite('foundSquares.jpg',img)
        ch = cv.waitKey()
        if ch == 27:
            break
    
    return squares


if __name__ == '__main__':
    print(__doc__)
    detect()
    cv.destroyAllWindows()