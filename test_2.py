# -*- coding: utf-8 -*-
# @Time   : 19-8-8 上午8:56
# @Author : huziying
# @File   : test_2.py

import cv2
import numpy

# todo find circles......

image = cv2.imread('/home/dsd/Desktop/circuit_board/分类（红线为检测位置)/坏的形状（这类一般识别挑出来）/1565144166.png')
# image = cv2.imread('/home/dsd/Desktop/circuit_board/circle.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# thres = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)[1]

cv2.namedWindow('blurred', cv2.WINDOW_NORMAL)
cv2.imshow("blurred", blurred)
cv2.waitKey(0)

# cv2.namedWindow('thres', cv2.WINDOW_NORMAL)
# cv2.imshow("thres", thres)
# cv2.waitKey(0)

# edges = cv2.Canny(gray, 30, 100)
#
# cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
# cv2.imshow("edges", edges)
# cv2.waitKey(0)

# output = blurred.copy()

# detect circles in the image
circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, 30, minRadius=10, maxRadius=50)
# circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, 30)

print('circles', circles)
if circles is not None:
    print(len(circles))

# if circles is not None:
#     # convert the (x, y) coordinates and radius of the circles to integers
#     circles = numpy.round(circles[0, :]).astype("int")
#
#     # loop over the (x, y) coordinates and radius of the circles
#     for (x, y, r) in circles:
#         # draw the circle in the output image, then draw a rectangle
#         # corresponding to the center of the circle
#         cv2.circle(output, (x, y), r, (0, 255, 0), 4)
#         cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
#
#     # show the output image
#     cv2.imshow("output", output)
#     # tmp = cv2.Canny(image,200,400,3)
#     cv2.waitKey(0)
