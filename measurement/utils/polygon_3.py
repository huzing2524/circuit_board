# -*- coding: utf-8 -*-
# @Time   : 19-8-19 下午4:29
# @Author : huziying
# @File   : polygon_3.py

import cv2
import numpy
import uuid
import base64
import os


def a_measurement(coordinates, img):
    """宽度"""
    bottom = coordinates[coordinates.argmax(axis=0)[1]]
    print("bottom", bottom)
    cv2.circle(img, tuple(bottom), 6, (0, 0, 255), 6)


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/polygon_3.jpg')
    else:
        receive = base64.b64decode(image)
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(receive)
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))

    # todo 颜色区分...噪点太多，感觉无法定位
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_blurred = cv2.bilateralFilter(img_hsv, 9, 100, 15)

    # 黄色
    lower_yellow = numpy.array([26, 43, 46])
    upper_yellow = numpy.array([34, 255, 255])
    mask = cv2.inRange(img_blurred, lower_yellow, upper_yellow)
    res = cv2.bitwise_and(img, img, mask=mask)

    edges = cv2.Canny(mask, 200, 400, 1)
    indices = numpy.where(edges != [0])
    coordinates = numpy.array(list(zip(indices[1], indices[0])))

    for e in coordinates:
        cv2.circle(img, tuple(e), 1, (0, 255, 0), 1)

    a_measurement(coordinates, img)

    if os.path.exists('measurement/images/{}.jpg'.format(img_name)):
        os.remove('measurement/images/{}.jpg'.format(img_name))

    # cv2.namedWindow('img_hsv', cv2.WINDOW_NORMAL)
    # cv2.imshow("img_hsv", img_hsv)
    # cv2.waitKey(0)

    # cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
    # cv2.imshow("mask", mask)
    # cv2.waitKey(0)

    # cv2.namedWindow('res', cv2.WINDOW_NORMAL)
    # cv2.imshow("res", res)
    # cv2.waitKey(0)

    # cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
    # cv2.imshow("edges", edges)
    # cv2.waitKey(0)

    # cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)

    # cv2.destroyAllWindows()

    return {}


if __name__ == '__main__':
    main()
