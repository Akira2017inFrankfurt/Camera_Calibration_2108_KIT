import cv2 as cv
from matplotlib import pyplot as plt

# todo: to understand
# cv.StereoBM_create()
# stereo.compute()

imgL = cv.imread('/Users/Haruki/test_opencv/tsukuba_l.png', 0)
imgR = cv.imread('/Users/Haruki/test_opencv/tsukuba_r.png', 0)
stereo = cv.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(imgL, imgR)
plt.imshow(disparity, 'gray')
plt.show()
