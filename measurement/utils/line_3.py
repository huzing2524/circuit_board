# -*- coding: utf-8 -*-
# @Time   : 19-8-21 下午4:51
# @Author : huziying
# @File   : line_3.py

import cv2
import numpy
import uuid
import base64
import os


def a_b_measurement(coordinates, img):
    """上面竖直位置 a, 下面 竖直位置 b"""
    pass


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/line_2.jpg')
    else:
        receive = base64.b64decode(image)
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(receive)
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blurred = cv2.bilateralFilter(img_gray, 0, 100, 15)
    img_thresh = cv2.threshold(img_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # OTSU滤波, 自动找到一个介于两波峰之间的阈值

    edges = cv2.Canny(img_thresh, 200, 400, 1)

    indices = numpy.where(edges != [0])
    coordinates = numpy.array(list(zip(indices[1], indices[0])))

    a_b_measurement(coordinates, img)

    if os.path.exists('measurement/images/{}.jpg'.format(img_name)):
        os.remove('measurement/images/{}.jpg'.format(img_name))

    # cv2.namedWindow('img_thresh', cv2.WINDOW_NORMAL)
    # cv2.imshow("img_thresh", img_thresh)
    # cv2.waitKey(0)

    cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
    cv2.imshow("edges", edges)
    cv2.waitKey(0)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
