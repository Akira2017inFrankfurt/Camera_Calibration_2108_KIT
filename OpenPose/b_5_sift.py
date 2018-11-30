# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28.11.2018

@author: Liang
"""

import cv2
import numpy as np

filepath = '/Users/Haruki/Desktop/建筑物.jpg'
img = cv2.imread(filepath)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 存在问题，需要修改
sift = cv2.xfeatures2d_SIFT()
kp = sift.detect(sift, gray, None)

img = cv2.drawKeypoints(gray, kp)
cv2.imwrite('sift_keypoints.jpg', img)