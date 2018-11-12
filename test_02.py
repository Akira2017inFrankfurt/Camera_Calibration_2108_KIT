# do something about calibration, undistortion
# after obtaining the results, can storage the camera matrix and distortion coefficients for future reuse
import cv2 as cv
import numpy as np
from test_01 import objpoints, imgpoints, gray

# todo: to understand belows
# cv2.calibrateCamera()
# cv2.getOptimalNewCameraMatrix()
# cv2.undistort() important
# the solution of dst
# generation and name of cv2, and how to storage in system


ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# take left12.jpg as example
img = cv.imread('/Users/Haruki/test_opencv/left12.jpg')
h, w = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

# the easiest way:  Just call the function
# and use ROI obtained above to crop the result

# undistort
dst = cv.undistort(img, mtx, dist, None, newcameramtx)

# crop the image
x, y, w, h = roi
dst = dst[y:y + h, x:x + w]
cv.imwrite('calibresult12_01.png', dst)

# re-projection error
# provides a good estimation of how exact the found paras are.
# the closer the re-p error to 0 is, the more accurate the paras are.


mean_error = 0
for i in xrange(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)

# todo: the value is 0? right or not?
print "total error: {}".format(mean_error / len(objpoints))

np.savez('B.npz', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)
