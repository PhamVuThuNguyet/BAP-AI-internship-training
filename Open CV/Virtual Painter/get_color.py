import cv2.cv2 as cv2
import numpy as np

# define capture device use laptop camera
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)


# create trackbars to set the values of upper and lower limit of H,S,V
def trackbar_onchange(x):
    pass


cv2.namedWindow("trackbar")
cv2.createTrackbar("L-H", "trackbar", 0, 179, trackbar_onchange)
cv2.createTrackbar("L-S", "trackbar", 0, 255, trackbar_onchange)
cv2.createTrackbar("L-V", "trackbar", 0, 255, trackbar_onchange)
cv2.createTrackbar("U-H", "trackbar", 179, 179, trackbar_onchange)
cv2.createTrackbar("U-S", "trackbar", 255, 255, trackbar_onchange)
cv2.createTrackbar("U-V", "trackbar", 255, 255, trackbar_onchange)

while True:
    ret, frame = capture.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L-H", "trackbar")
    l_s = cv2.getTrackbarPos("L-S", "trackbar")
    l_v = cv2.getTrackbarPos("L-V", "trackbar")
    h_h = cv2.getTrackbarPos("U-H", "trackbar")
    h_s = cv2.getTrackbarPos("U-S", "trackbar")
    h_v = cv2.getTrackbarPos("U-V", "trackbar")

    low = np.array([l_h, l_s, l_v])
    high = np.array([h_h, h_s, h_v])

    mask = cv2.inRange(hsv, low, high)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow("result", result)

    key = cv2.waitKey(1)
    # If the user presses `s` then print and save this array.
    if key == ord('s'):
        color_array = [[l_h, l_s, l_v], [h_h, h_s, h_v]]
        # Save this array as penrange.npy
        np.save('pen_range', color_array)
        break
    # if esc pressed exit
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()
