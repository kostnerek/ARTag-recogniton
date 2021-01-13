import cv2 as cv2
import numpy as np
import pygame.camera
import math, glob, pathlib

def check(original, image_to_compare, fileToWrite, savePicture = False):
    original = cv2.imread(original)
    image_to_compare = cv2.imread(image_to_compare)

    #Check for similarities between the 2 images
    sift = cv2.xfeatures2d.SIFT_create()
    kp_1, desc_1 = sift.detectAndCompute(original, None)
    kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)

    index_params = dict(algorithm=0, trees=5)
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(desc_1, desc_2, k=2)

    good_points = []
    for m, n in matches:
        if m.distance < 0.6*n.distance:
            good_points.append(m)

    # Define how similar they are
    number_keypoints = 0
    if len(kp_1) <= len(kp_2):
        number_keypoints = len(kp_1)
    else:
        number_keypoints = len(kp_2)
        
    if(savePicture==True):
        name="photos/similarityResult/"
        name+=str(fileToWrite)
        name+=".jpg"
        result = cv2.drawMatches(original, kp_1, image_to_compare, kp_2, good_points, None)
        cv2.resize(result, None, fx=0.4, fy=0.4)
        cv2.imwrite(str(name), result)
    
    return len(good_points) / number_keypoints * 100

def checkSimilarity(_END_PHOTO_PATH_, showValues=False, savePicture = False):
    projectPath = str(pathlib.Path(__file__).parent.absolute())
    projectPathLen = len(projectPath)
    projectPath+="\\templates\\*.*"
    files = glob.glob(projectPath)
    checkVal=[]

    for x in range(len(files)):
        name="."
        name+=files[x][projectPathLen:]
        simPercent=math.ceil(check(name,_END_PHOTO_PATH_,x,savePicture))
        if(showValues==True):
            print(simPercent,'%')
        checkVal.append(simPercent)

    _ARTagCode = checkVal.index(max(checkVal))
    if(showValues==True):
        print('Encoded number is: ', _ARTagCode+1)
    return _ARTagCode+1