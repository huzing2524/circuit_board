# -*- coding: utf-8 -*-
# @Time   : 19-8-22 上午10:28
# @Author : huziying
# @File   : circuit_surface.py

import cv2
import numpy
import uuid
import base64
import os


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/circuit_surface.jpg')
    else:
        receive = base64.b64decode(image)
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(receive)
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blurred = cv2.bilateralFilter(img_gray, 0, 100, 15)
    img_thresh = cv2.threshold(img_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # OTSU滤波, 自动找到一个介于两波峰之间的阈值

    # edges = cv2.Canny(img_thresh, 200, 400, 1)
    # indices = numpy.where(edges != [0])
    # coordinates = numpy.array(list(zip(indices[1], indices[0])))

    # todo 先裁剪出来中间的部分，然后用颜色区分检测边缘...

    # a_b_c_measurement(coordinates, img)

    if os.path.exists('measurement/images/{}.jpg'.format(img_name)):
        os.remove('measurement/images/{}.jpg'.format(img_name))

    cv2.namedWindow('img_thresh', cv2.WINDOW_NORMAL)
    cv2.imshow("img_thresh", img_thresh)
    cv2.waitKey(0)

    # cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
    # cv2.imshow("edges", edges)
    # cv2.waitKey(0)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
