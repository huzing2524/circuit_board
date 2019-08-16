# -*- coding: utf-8 -*-
# @Time   : 19-8-7 下午5:12
# @Author : huziying
# @File   : test.py

import cv2
import numpy
import imutils

# todo match template......

# todo first: cv2.matchShapes
"""比较两个形状或者轮廓的相似度，如果返回值越小，匹配越好"""

template = cv2.imread('/home/dsd/Desktop/circuit_board/template/polygon_2.png', 0)
thresh = cv2.threshold(template, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cnts_1 = contours[0]

cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)
cv2.imshow("thresh", thresh)
cv2.waitKey(0)

image = cv2.imread('/home/dsd/Desktop/circuit_board/测试图/正常标准图03.jpg', 0)
thresh2 = cv2.threshold(image, 127, 255, 0)[1]
contours_2, hierarchy_2 = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts_2 = contours_2[0]

cv2.namedWindow('thresh2', cv2.WINDOW_NORMAL)
cv2.imshow("thresh2", thresh2)
cv2.waitKey(0)

# print(len(cnts_1), len(cnts_2))
ret = cv2.matchShapes(cnts_1, cnts_2, 1, 0)
print(ret)

cv2.destroyAllWindows()

# todo second: cv2.matchTemplate
# template image
# template = cv2.imread('/home/dsd/Desktop/circuit_board/template/half_circle_1.jpg', 0)
# H, W = template.shape
# template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
# template_blurred = cv2.GaussianBlur(template_gray, (5, 5), 0)
# template_thresh = cv2.threshold(template_blurred, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
# edges = cv2.Canny(template_thresh, 200, 400, 3)

# cv2.namedWindow('template', cv2.WINDOW_NORMAL)
# cv2.imshow("template", template)
# cv2.waitKey(0)

# orb = cv2.ORB_create(50000, scoreType=cv2.ORB_FAST_SCORE, nlevels=20, edgeThreshold=5)
# kp1, des1 = orb.detectAndCompute(edges, None)
# tmp_keys = cv2.drawKeypoints(edges, kp1, outImage=numpy.array([]), color=(0, 255, 0), flags=0)

# match image
# image = cv2.imread('/home/dsd/Desktop/circuit_board/测试图/正常标准图01.jpg')
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# thresh = cv2.threshold(blurred, 190, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
# edges_2 = cv2.Canny(thresh, 200, 400, 3)

# cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)
# print('cnts', cnts)

# result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
# print('result', result)
#
# threshold = 0.7
# loc = numpy.where(result >= threshold)
# for pt in zip(*loc[::-1]):
#     cv2.rectangle(image, pt, (pt[0] + W, pt[1] + H), (0, 0, 255), 2)


# cv2.namedWindow('template', cv2.WINDOW_NORMAL)
# cv2.imshow("template", template)
# cv2.waitKey(0)

# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# cv2.imshow("image", image)
# cv2.waitKey(0)
#
# cv2.destroyAllWindows()
