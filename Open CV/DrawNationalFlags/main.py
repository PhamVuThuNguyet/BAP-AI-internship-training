from math import sqrt, cos, sin, pi
import numpy as np
import cv2.cv2 as cv2

flag = np.zeros((300, 600, 3), np.uint8)


def dda_algo(d, xa, ya, xb, yb):
    dx = xb - xa
    dy = yb - ya
    steps = max(abs(dx), abs(dy))
    x_inc = dx / steps
    y_inc = dy / steps
    d[xa, ya] = 1
    x = float(xa)
    y = float(ya)
    for i in range(steps - 1):
        x += x_inc
        y += y_inc
        x_round = int(round(x, 0))
        y_round = int(round(y))
        d[x_round, y_round] = 1
    return d


def dda_algo_for_star(star, r, x_center, y_center):
    x = np.zeros((5, 1), dtype=int)
    y = np.zeros((5, 1), dtype=int)
    x[0] = x_center - r
    y[0] = y_center

    grad = (72 * pi) / 180

    for i in range(1, 5):
        x[i] = int(
            x[0] * cos(i * grad) - y[0] * sin(i * grad) + y_center * sin(i * grad) + x_center * (1 - cos(i * grad)))
        y[i] = int(
            x[0] * sin(i * grad) + y[0] * cos(i * grad) + y_center * (1 - cos(i * grad)) - x_center * sin(i * grad))

    for i in range(5):
        star[x[i], y[i]] = 1

    star = dda_algo(star, x[0][0], y[0][0], x[2][0], y[2][0])
    star = dda_algo(star, x[0][0], y[0][0], x[3][0], y[3][0])
    star = dda_algo(star, x[1][0], y[1][0], x[3][0], y[3][0])
    star = dda_algo(star, x[1][0], y[1][0], x[4][0], y[4][0])
    star = dda_algo(star, x[2][0], y[2][0], x[4][0], y[4][0])

    for i in range(star.shape[0]):
        for j in range(star.shape[1]):
            if star[i][j] == 1:
                break
            else:
                star[i][j] = -1
        for j in range(star.shape[1] - 1, -1, -1):
            if star[i][j] == 1:
                break
            star[i][j] = -1
    for j in range(star.shape[1]):
        for i in range(star.shape[0]):
            if star[i][j] == 1:
                break
            else:
                star[i][j] = -1
        for i in range(star.shape[0] - 1, -1, -1):
            if star[i][j] == 1:
                break
            star[i][j] = -1

    return star


def japan_flag():
    center_x, center_y = 150, 300
    radius = 100
    flag[:, :, :] = 255
    # crimson glory
    crimson_glory = np.array([50, 0, 190])
    # Draw a circle with crimson glory color
    # loop for rows i.e. for x-axis
    for i in range(50, 251):
        # loop for columns i.e. for y-axis
        for j in range(200, 401):
            distance = sqrt((center_x - i) ** 2 + (center_y - j) ** 2)
            if distance <= radius:
                # fill the circle with crimson glory
                # color using RGB color representation.
                flag[i, j, :] = crimson_glory
    return flag


def sweden_flag():
    # blue
    flag[:, :, 0] = 255

    # yellow stripe
    yellow = np.array([0, 255, 255])
    flag[120:181, :, :] = yellow
    flag[:, 150:211, :] = yellow
    return flag


def thailand_flag():
    vivid_burgundy = np.array([49, 25, 165])
    space_cadet = np.array([74, 42, 45])
    cultured = np.array([248, 245, 244])

    flag[:100, :, :] = vivid_burgundy
    flag[100:200, :, :] = cultured
    flag[200:400, :, :] = space_cadet
    flag[400:500, :, :] = cultured
    flag[500:600, :, :] = vivid_burgundy
    return flag


def france_flag():
    usafa_blue = np.array([164, 85, 0])
    white = np.array([255, 255, 255])
    cinnabar = np.array([53, 65, 239])

    flag[:, :200, :] = usafa_blue
    flag[:, 200:400, :] = white
    flag[:, 400:600, :] = cinnabar
    return flag


def vietnam_flag():
    star = np.zeros((300, 600))
    star = dda_algo_for_star(star, 100, 150, 300)

    maximum_red = np.array([29, 37, 218])
    tangerine_yellow = np.array([0, 205, 255])

    flag[:, :, :] = maximum_red
    for i in range(flag.shape[0]):
        for j in range(flag.shape[1]):
            if star[i][j] == -1:
                flag[i][j] = maximum_red
            else:
                flag[i][j] = tangerine_yellow

    return flag


def show_img(flag_to_show):
    cv2.imshow("Flag", flag_to_show)
    cv2.waitKey()


vietnam_flag()
show_img(flag)
