import math
import numpy as np
import cv2.cv2 as cv2

flag = np.zeros((300, 600, 3), np.uint8)

center_x, center_y = 150, 300
radius = 50

flag[:, :, :] = 255

# Draw a circle with crimson glory color
# loop for rows i.e. for x-axis
for i in range(100, 201):
    # loop for columns i.e. for y-axis
    for j in range(250, 351):
        distance = math.sqrt((center_x - i) ** 2 + (center_y - j) ** 2)
        if distance <= radius:
            # fill the circle with crimson glory
            # color using RGB color representation.
            flag[i, j, 0] = 45
            flag[i, j, 1] = 0
            flag[i, j, 2] = 188

cv2.imshow("Japan Flag", flag)
cv2.waitKey()
