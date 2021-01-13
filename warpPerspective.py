import cv2
import math
import numpy as np
import matplotlib.pyplot as plt


def warp(img_name,coords):
    img = cv2.imread(img_name)
    rows,cols,ch = img.shape

    #pts1 = np.float32([[31,79],[388,97],[375,447],[15,433]])
    pts1 = np.float32(coords)

    ratio=1
    cardH=math.sqrt((pts1[2][0]-pts1[1][0])*(pts1[2][0]-pts1[1][0])+(pts1[2][1]-pts1[1][1])*(pts1[2][1]-pts1[1][1]))
    cardW=ratio*cardH;
    pts2 = np.float32([[pts1[0][0],pts1[0][1]], [pts1[0][0]+cardW, pts1[0][1]], [pts1[0][0]+cardW, pts1[0][1]+cardH], [pts1[0][0], pts1[0][1]+cardH]])

    M = cv2.getPerspectiveTransform(pts1,pts2)

    offsetSize=500
    transformed = np.zeros((int(cardW+offsetSize), int(cardH+offsetSize)), dtype=np.uint8);
    dst = cv2.warpPerspective(img, M, transformed.shape)

    cv2.imwrite('photos/warpedPerspective.jpg', dst)

