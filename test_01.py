# obtain object points and image points

import numpy as np
import cv2 as cv
import glob

# todo: have to figure out these functions and parameters
# TERM_CRITERIA_EPS:
# TERM_CRITERIA_MAX_ITER:
# numpy.mgrid():
# cv2.cvtColor():
# cv2.findChessboardCorners():
# cv2.cornerSubPix():
# and the way to get the expected points:


# termination criteria
# when to stop
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)  # print type(criteria) = tuple

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6 * 7, 3), np.float32)  # numpy.n_d_array, 42
objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)  # generate the points as expected

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

# the function of glob.glob is to find all the correspond file, based on the given file path
# so, here we have to offer the function with legal parameter
images = glob.glob('/Users/Haruki/test_opencv/*.jpg')  # list

# print len(images)

for f_name in images:

    # img and gray are both n_d_array
    img = cv.imread(f_name)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    # type of ret is bool
    ret, corners = cv.findChessboardCorners(gray, (7, 6), None)

    # If found, add object points, image points (after refining them)
    if ret:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)  # n_d_array
        imgpoints.append(corners)

        # Draw and display the corners
        cv.drawChessboardCorners(img, (7, 6), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(1500)  # the time pause between the pictures to show

cv.destroyAllWindows()