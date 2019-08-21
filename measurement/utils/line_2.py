# -*- coding: utf-8 -*-
# @Time   : 19-8-21 下午4:51
# @Author : huziying
# @File   : line_2.py

import cv2
import numpy
import uuid
import base64
import os


def a_measurement(coordinates, img):
    """中间 竖直位置 a"""
    left = coordinates[coordinates.argmin(axis=0)[0]]
    # print("left", left)
    whole_array = coordinates[numpy.where(coordinates[:, 0] == left[0])]
    # print("whole_array", whole_array)
    top_limit = coordinates[numpy.where(
        (coordinates[:, 1] >= whole_array[0][1] - 30) & (coordinates[:, 1] <= whole_array[1][1] + 30))]
    # print("top_limit", top_limit)
    # for t in top_limit:
    #     cv2.circle(img, tuple(t), 1, (255, 0, 0), 1)

    top_left = top_limit[top_limit.argmin(axis=0)[0]]
    top_right = top_limit[top_limit.argmax(axis=0)[0]]
    # print("top_left", top_left), print("top_right", top_right)

    a_x = top_left[0] + int(((top_right[0] - top_left[0]) / 4 * 3))
    a_top_coordinate = top_limit[numpy.where(top_limit[:, 0] == a_x)][-1]
    a_bottom_coordinate = coordinates[numpy.where(
        (coordinates[:, 0] == a_top_coordinate[0]) & (coordinates[:, 1] > a_top_coordinate[1]))][0]
    # print("a_top_coordinate", a_top_coordinate, "a_bottom_coordinate", a_bottom_coordinate)
    cv2.line(img, tuple(a_top_coordinate), tuple(a_bottom_coordinate), (255, 0, 0), thickness=4)
    cv2.putText(img, str(a_bottom_coordinate[1] - a_top_coordinate[1]),
                (a_top_coordinate[0] + 10, a_top_coordinate[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4)


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

    a_measurement(coordinates, img)

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
