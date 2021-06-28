import numpy as np
import cv2.cv2 as cv

image = np.zeros((600, 800, 3), np.uint8)

image[:100, :, 0] = 49
image[:100, :, 1] = 25
image[:100, :, 2] = 165

image[100:200, :, 0] = 248
image[100:200, :, 1] = 245
image[100:200, :, 2] = 244

image[200:400, :, 0] = 72
image[200:400, :, 1] = 44
image[200:400, :, 2] = 45

image[400:500, :, 0] = 248
image[400:500, :, 1] = 245
image[400:500, :, 2] = 244

image[500:600, :, 0] = 49
image[500:600, :, 1] = 25
image[500:600, :, 2] = 165

cv.imshow('ThaiLand Flag', image)
cv.waitKey()
