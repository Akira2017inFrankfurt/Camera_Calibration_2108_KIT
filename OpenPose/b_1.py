import cv2 as cv

img = cv.imread('/Users/Haruki/test_opencv/myleft.jpg', cv.IMREAD_COLOR)
cv.namedWindow('image', cv.WINDOW_NORMAL)
cv.imshow('image', img)

# for 64bit system
k = cv.waitKey(0) & 0xFF

if k == 27:
    # wait for ESC key to exit
    cv.destroyAllWindows('image')