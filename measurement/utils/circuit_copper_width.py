# -*- coding: utf-8 -*-
# @Time   : 19-8-23 下午3:58
# @Author : huziying
# @File   : circuit_copper_width.py

import cv2
import numpy
import uuid
import base64
import os


def a_b_measurement(coordinates, img):
    """会有多个 部分尺寸测量 整体宽度 里面的部分位置和背景噪声很像，无法识别测量"""
    bottom = coordinates[coordinates.argmax(axis=0)[1]]
    # print("bottom", bottom)
    bottom_array = coordinates[numpy.where(coordinates[:, 0] == bottom[0])]
    # print("bottom_array", bottom_array)
    width_limit = coordinates[numpy.where(
        (coordinates[:, 1] >= bottom_array[-2][1] - 100) & (coordinates[:, 1] <= bottom_array[-1][1] + 100))]
    coordinates_limit_sort = width_limit[width_limit[:, 0].argsort(), :]
    # print("coordinates_limit_sort", coordinates_limit_sort)
    count_list = list()
    for index in range(len(coordinates_limit_sort) - 1):
        if coordinates_limit_sort[index + 1][0] - coordinates_limit_sort[index][0] > 50:
            count_list.append(index)
    # print("count_list", count_list)
    # todo 多个物体自动测量
    a_x_left, a_x_right = coordinates_limit_sort[0][0], coordinates_limit_sort[count_list[0]][0]
    b_x_left, b_x_right = coordinates_limit_sort[count_list[0] + 1][0], coordinates_limit_sort[-1][0]
    # print(a_x_left, a_x_right), print(b_x_left, b_x_right)
    a_middle = a_x_left + (a_x_right - a_x_left) // 2
    a_coordinates_array = coordinates[numpy.where(coordinates[:, 0] == a_middle)]
    a_coordinate_top, a_coordinate_bottom = a_coordinates_array[-2], a_coordinates_array[-1]
    a_length = a_coordinate_bottom[1] - a_coordinate_top[1]
    cv2.line(img, tuple(a_coordinate_top), tuple(a_coordinate_bottom), (255, 0, 0), thickness=4)
    cv2.putText(img, str(a_length), (a_coordinate_top[0] + 10, a_coordinate_top[1] + 50),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4)

    b_middle = b_x_left + (b_x_right - b_x_left) // 2
    b_coordinates_array = coordinates[numpy.where(coordinates[:, 0] == b_middle)]
    b_coordinate_top, b_coordinate_bottom = b_coordinates_array[-2], b_coordinates_array[-1]
    b_length = b_coordinate_bottom[1] - b_coordinate_top[1]
    # print("a_coordinates_array", a_coordinates_array), print("b_coordinates_array", b_coordinates_array)
    cv2.line(img, tuple(b_coordinate_top), tuple(b_coordinate_bottom), (255, 0, 0), thickness=4)
    cv2.putText(img, str(b_length), (b_coordinate_top[0] + 10, b_coordinate_top[1] + 50),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4)


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/circuit_copper_width.jpg')
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
