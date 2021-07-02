import cv2.cv2 as cv2
import numpy as np


def drawing_on_screen():
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # loading HSV range
    pen_range = np.load('pen_range.npy')
    print(pen_range)
    # initializing empty screen
    screen = None
    # initializing position on pen
    x1, y1, x2, y2 = 0, 0, 0, 0
    while True:
        # read new frame
        success, frame = capture.read()
        # flip horizontally
        frame = cv2.flip(frame, 1)
        if screen is None:
            # initializing black screen
            screen = np.zeros_like(frame)

        hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_range = pen_range[0]
        upper_range = pen_range[1]
        mask = cv2.inRange(hsv_img, lower_range, upper_range)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        contour_area = 0
        try:
            contour_area = cv2.contourArea(max(contours, key=cv2.contourArea))
        except ValueError as e:
            print(e)

        if contours and contour_area > 100:
            c = max(contours, key=cv2.contourArea)
            x2, y2, w, h = cv2.boundingRect(c)

            if x1 == 0 and y1 == 0:
                x1 = x2
                y1 = y2
            else:
                screen = cv2.line(screen, (x1, y1), (x2, y2), [0, 170, 255], 10)
            x1 = x2
            y1 = y2
        frame = cv2.addWeighted(frame, 0.7, screen, 0.3, 0)
        stacked = np.hstack((frame, screen))
        cv2.imshow("abc", stacked)

        if cv2.waitKey(1) & 0xFF == ord("c"):
            screen = np.zeros_like(frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    drawing_on_screen()
