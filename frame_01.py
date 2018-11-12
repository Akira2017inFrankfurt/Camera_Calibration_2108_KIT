import cv2 as cv

# new an object of cv2.VideoCapture
video_capture = cv.VideoCapture()
# open the file path
video_capture.open('/Users/Haruki/Desktop/tree.avi')

# get the fps of the video
fps = int(video_capture.get(cv.CAP_PROP_FPS))  # float todo: use int() is not perfect, for example 14.999 = 14 not 15

# get the total number of the video
frames = video_capture.get(cv.CAP_PROP_FRAME_COUNT)  # float

# print 'fps type:', type(fps), 'frames type:', type(frames)
# print 'fps:', fps, 'frames:', frames

# storage the frames of the video:
# here is not all the frames
for i in range(1):
    ret, frame = video_capture.read()  # ret is bool; frame is n_d_array
    cv.imwrite('/Users/Haruki/Desktop/(%d).jpg' % i, frame)
    # print 'ret type:', type(ret), 'frame type:', type(frame)
