# -*- coding: utf-8 -*-
# @Time   : 19-8-19 下午5:06
# @Author : huziying
# @File   : polygon_4.py

import cv2
import numpy
import uuid
import base64
import os


def a_b_c_measurement(coordinates, img):
    """部分位置的尺寸: 断口宽度 a, 两条线之间的宽度 b, 下面线条的长度 c"""
    left = coordinates[coordinates.argmin(axis=0)[0]]
    right = coordinates[coordinates.argmax(axis=0)[0]]
    # print(left), print(right)
    middle_list = list()
    for index in range(right[0] - left[0]):
        search = coordinates[numpy.where(coordinates[:, 0] == index)]
        if len(search) > 0:
            if abs(search[0][1] - left[1]) > 50:
                middle_list.append(index - 1)
                break
    a_left = coordinates[numpy.where(coordinates[:, 0] == middle_list[0])][0]

    # print("middle_list", middle_list)
    a_right_coordinate = coordinates[numpy.where((coordinates[:, 1] == a_left[1]) & (coordinates[:, 0] != a_left[0]))]
    a_temp_list = list()
    for index in range(len(a_right_coordinate[:, 0])):
        if a_right_coordinate[index][0] - a_left[0] > 50:
            a_temp_list.append(index)
            break
    a_right = a_right_coordinate[a_temp_list[0]]
    # print("a_left", a_left), print("a_right", a_right)

    cv2.line(img, tuple(a_left), tuple(a_right), (255, 0, 0), thickness=4)
    cv2.putText(img, str(a_right[0] - a_left[0]), (a_left[0] + 10, a_left[1] - 30), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    a_coordinate = coordinates[numpy.where(coordinates[:, 0] == a_left[0])]
    # print("a_coordinate", a_coordinate)
    bottom_limit = coordinates[numpy.where(
        (coordinates[:, 1] >= (a_coordinate[-2][1] - 20)) & (coordinates[:, 1] <= (a_coordinate[-1][1] + 20)))]
    # for c in bottom_limit:
    #     cv2.circle(img, tuple(c), 1, (0, 255, 0), 1)
    c_left = bottom_limit[bottom_limit.argmin(axis=0)[0]]
    c_right = bottom_limit[numpy.where(bottom_limit[:, 1] == c_left[1])][-1]
    # print("c_left", c_left), print("c_right", c_right)

    cv2.line(img, tuple(c_left), tuple(c_right), (255, 0, 0), thickness=4)
    cv2.putText(img, str(c_right[0] - c_left[0]), (c_left[0] + 10, c_left[1] + 70),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4)

    b_x = a_right[0] + (c_right[0] - a_right[0]) // 2
    # print("b_x", b_x)
    b_coordinate = coordinates[numpy.where(coordinates[:, 0] == b_x)]
    # print("b_coordinate", b_coordinate)
    b_coordinate_x, b_coordinate_y = b_coordinate[1], b_coordinate[2]
    cv2.line(img, tuple(b_coordinate_x), tuple(b_coordinate_y), (255, 0, 0), thickness=4)
    cv2.putText(img, str(b_coordinate_y[1] - b_coordinate_x[1]), (b_coordinate_x[0] + 10, b_coordinate_x[1] + 50),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4)


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/polygon_4.jpg')
    else:
        receive = base64.b64decode(image)
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(receive)
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img_blurred = cv2.GaussianBlur(img_gray, (55, 55), 0)
    # img_blurred = cv2.bilateralFilter(img_gray, 0, 100, 15)
    img_blurred = cv2.bilateralFilter(img_gray, 9, 75, 75)
    # 灰度: 白色为255, 黑色为0
    img_thresh = cv2.threshold(img_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # OTSU滤波, 自动找到一个介于两波峰之间的阈值
    # img_thresh = cv2.threshold(img_blurred, 127, 255, 0)[1]  # 简单滤波
    # img_thresh = cv2.adaptiveThreshold(img_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    edges = cv2.Canny(img_thresh, 200, 400, 1)  # shape (1944, 2592)

    indices = numpy.where(edges != [0])
    coordinates = numpy.array(list(zip(indices[1], indices[0])))

    a_b_c_measurement(coordinates, img)

    if os.path.exists('measurement/images/{}.jpg'.format(img_name)):
        os.remove('measurement/images/{}.jpg'.format(img_name))

    cv2.namedWindow('img_thresh', cv2.WINDOW_NORMAL)
    cv2.imshow("img_thresh", img_thresh)
    cv2.waitKey(0)

    cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
    cv2.imshow("edges", edges)
    cv2.waitKey(0)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
