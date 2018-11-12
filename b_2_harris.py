import cv2 as cv
import numpy as np

filename = '/Users/Haruki/test_opencv/left01.jpg'
img = cv.imread(filename)

# convert common images to gray images
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# convert images to n_d_array
gray = np.float32(gray)

# the parameters of Harris:
# img: type is float32
# blockSize: the size of area to consider
# ksize: in Sobel Derivation, size of the window
# k: in [0.04, 0.06]
dst = cv.cornerHarris(gray, 2, 3, 0.04)

# result is dilated for marking the corners, not important
# dilated: make bigger
dst = cv.dilate(dst, None)

# threshold for an optional value, it may vary depending on the image
img[dst > 0.01 * dst.max()] = [0, 0, 255]

cv.imshow('dst', img)
if cv.waitKey(0) & 0xFF == 27:
    cv.destroyAllWindows()
