# use camera to capture videos and storage them
# todo: can work but have problems
import cv2 as cv

cap = cv.VideoCapture(0)

# define the codec and create VideoWriter object
# based on different system
# use Use 'mp4v' or 'avc1' for mac
fourcc = cv.VideoWriter_fourcc(*'avc1')
out = cv.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        frame = cv.flip(frame, 0)

        # write the filpped frame
        out.write(frame)

        cv.imshow('frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# release everything if job is finished
cap.release()
out.release()
cv.destroyAllWindows()
