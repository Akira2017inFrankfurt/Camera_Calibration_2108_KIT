"""
Created on Thu Nov 08

@author: Haruki
"""

import cv2 as cv
import numpy as np

filename = '/Users/Haruki/test_opencv/left01.jpg'
img = cv.imread(filename)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# find Harris corners
gray = np.float32(gray)
dst = cv.cornerHarris(gray, 2, 3, 0.04)
dst = cv.dilate(dst, None)
ret, dst = cv.threshold(dst, 0.01 * dst.max(), 255, 0)
dst = np.uint8(dst)

# find centroids
ret, labels, stats, centroids = cv.connectedComponentsWithStats(dst)

# define the criteria to stop and refine the corners
criteria = (cv.TermCriteria_EPS + cv.TermCriteria_MAX_ITER, 100, 0.001)

# get the array of images
corners = cv.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria)

# draw them
res = np.hstack((centroids, corners))
# np.int0 loss the xiaoshu wei
res = np.int0(res)

img[res[:, 1], res[:, 0]] = [0, 0, 255]
img[res[:, 3], res[:, 2]] = [0, 255, 0]

cv.imwrite('subpixel5.png', img)
