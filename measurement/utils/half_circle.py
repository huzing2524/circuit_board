# -*- coding: utf-8 -*-
# @Time   : 19-8-5 下午5:31
# @Author : huziying
# @File   : half_circle.py

# 半圆形
import random

import cv2
import numpy
import uuid
import base64
import os

from django.db import connection

numpy.set_printoptions(threshold=numpy.inf)


def a_measurement(coordinates, img):
    """最左边点 a, 正常 半圆环型"""
    a_left = coordinates[coordinates.argmin(axis=0)[0]]  # 返回沿轴axis最大/小值的索引, 0代表列, 1代表行
    print("最左边", a_left)  # [74 383]
    coordinate = numpy.where((coordinates[:, 1] == a_left[1]) & (coordinates[:, 0] != a_left[0]))  # <class 'tuple'> 只取第2列的最大值, 剔除自身

    a_right = coordinates[coordinate][0]
    print("a_right", a_right, type(a_right))

    a_length = a_right[0] - a_left[0]
    # print("a_length", a_length, type(str(a_length))) [231 383]

    cv2.line(img, tuple(a_left), tuple(a_right), (255, 0, 0), thickness=2)
    cv2.putText(img, 'A {}'.format(a_length), (a_left[0] - 10, a_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (255, 0, 0), 2)

    cv2.rectangle()
    return a_right[0], a_length


def b_c_measurement(coordinates, img, a_right_x):
    """上 b, 下 c"""
    # random_distance = random.randint(0, distance)
    # b_x = random_distance + a_right_x
    # # print("b_d_left_x", b_d_left_x)
    # b_coordinate_array = coordinates[numpy.where(coordinates[:, 0] == b_x)]
    # index = numpy.argsort(b_coordinate_array[:, 1])  # 排序: 按照y坐标从上到下排列
    # temp = [b_coordinate_array[i] for i in index]
    # temp_2 = list()
    # # print('temp', temp, len(temp))
    # for t in range(len(temp) - 1):
    #     # print(t), print(temp[t + 1][1], temp[t][1])
    #     if temp[t + 1][1] - temp[t][1] >= 5:
    #         temp_2.append(temp[t + 1])
    #
    # temp_2.insert(0, temp[0])
    # # print('temp', temp, len(temp))
    # # print('temp_2', temp_2)
    # b_d_coordinate_array = numpy.array(temp_2)
    # # print("b_d_coordinate_array", b_d_coordinate_array)
    #
    # b_top, b_bottom = tuple(b_d_coordinate_array[index[0]]), tuple(b_d_coordinate_array[index[1]])
    # b_length = b_bottom[1] - b_top[1]
    #
    # cv2.line(img, b_top, b_bottom, (255, 0, 0), thickness=2)
    # cv2.putText(img, 'B {}'.format(b_length), (b_top[0] + 10, b_top[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),
    #             2)

    width_list_top = list()
    for x in range(a_right_x + 20, img.shape[1]):
        y_array = coordinates[numpy.where(coordinates[:, 0] == x)]
        # print(y_array)
        width_list_top.append(int(y_array[1][1]) - int(y_array[0][1]))

    # print("width_list_top", width_list_top)
    b_max_length = max(width_list_top)
    b_max_length_x = width_list_top.index(b_max_length) + a_right_x + 20
    b_max_coordinates = coordinates[numpy.where(coordinates[:, 0] == b_max_length_x)]
    b_max_coordinates_top, b_max_coordinates_bottom = b_max_coordinates[0], b_max_coordinates[1]
    cv2.line(img, tuple(b_max_coordinates_top), tuple(b_max_coordinates_bottom), (255, 0, 0), thickness=2)
    cv2.putText(img, 'B max {}'.format(b_max_length), (b_max_coordinates_top[0] + 10, b_max_coordinates_top[1] + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    b_min_length = min(width_list_top)
    b_min_length_x = width_list_top.index(b_min_length) + a_right_x + 20
    b_min_coordinates = coordinates[numpy.where(coordinates[:, 0] == b_min_length_x)]
    b_min_coordinates_top, b_min_coordinates_bottom = b_min_coordinates[0], b_min_coordinates[1]
    cv2.line(img, tuple(b_min_coordinates_top), tuple(b_min_coordinates_bottom), (255, 0, 0), thickness=2)
    cv2.putText(img, 'B min {}'.format(b_min_length), (b_min_coordinates_top[0] + 10, b_min_coordinates_top[1] + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    b_mean_length = sum(width_list_top) // len(width_list_top)
    # print("b_max_length", b_max_length, "b_max_length_x", b_max_length_x)
    # print("b_min_length", b_min_length, "b_min_length_x", b_min_length_x)
    # print("b_mean_length", b_mean_length)

    width_list_bottom = list()
    bottom_coordinates = coordinates[numpy.where(coordinates[:, 1] > b_max_coordinates_bottom[1] + 10)]
    for x in range(a_right_x + 20, img.shape[1]):
        y_array = bottom_coordinates[numpy.where(bottom_coordinates[:, 0] == x)]
        # print(y_array)
        width_list_bottom.append(int(y_array[-1][1]) - int(y_array[0][1]))

    # print('width_list_bottom', width_list_bottom)
    c_max_length = max(width_list_bottom)
    c_max_length_x = width_list_bottom.index(c_max_length) + a_right_x + 20
    c_max_coordinates = bottom_coordinates[numpy.where(bottom_coordinates[:, 0] == c_max_length_x)]
    c_max_coordinates_top, c_max_coordinates_bottom = c_max_coordinates[0], c_max_coordinates[-1]
    cv2.line(img, tuple(c_max_coordinates_top), tuple(c_max_coordinates_bottom), (255, 0, 0), thickness=2)
    cv2.putText(img, 'C max {}'.format(c_max_length), (c_max_coordinates_top[0] - 130, c_max_coordinates_top[1] + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    c_min_length = min(width_list_bottom)
    c_min_length_x = width_list_bottom.index(c_min_length) + a_right_x + 20
    c_min_coordinates = bottom_coordinates[numpy.where(bottom_coordinates[:, 0] == c_min_length_x)]
    c_min_coordinates_top, c_min_coordinates_bottom = c_min_coordinates[0], c_min_coordinates[-1]
    cv2.line(img, tuple(c_min_coordinates_top), tuple(c_min_coordinates_bottom), (255, 0, 0), thickness=2)
    cv2.putText(img, 'C min {}'.format(c_min_length), (c_min_coordinates_top[0] - 130, c_min_coordinates_top[1] + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    c_mean_length = sum(width_list_bottom) // len(width_list_bottom)

    return b_max_length, b_min_length, b_mean_length, c_max_length, c_min_length, c_mean_length


# def c_measurement(coordinates, img, distance, a_right_x):
#     """下 c"""
    # random_distance = random.randint(0, distance)
    # c_x = random_distance + a_right_x
    # c_coordinate_array = coordinates[numpy.where(coordinates[:, 0] == c_x)]
    # index = numpy.argsort(c_coordinate_array[:, 1])  # 排序: 按照y坐标从上到下排列
    # # print("c_e_coordinate_array", c_e_coordinate_array), print("index", index)
    # temp = [c_coordinate_array[i] for i in index]
    # temp_2 = list()
    # for t in range(len(temp) - 1):
    #     # print(t), print(temp[t + 1][1], temp[t][1])
    #     if temp[t + 1][1] - temp[t][1] >= 5:
    #         temp_2.append(temp[t + 1])
    # temp_2.insert(0, temp[0])
    # c_e_coordinate_array = numpy.array(temp_2)
    #
    # c_top, c_bottom = tuple(c_e_coordinate_array[index[0]]), tuple(c_e_coordinate_array[index[1]])
    # e_top, e_bottom = tuple(c_e_coordinate_array[index[2]]), tuple(c_e_coordinate_array[index[3]])
    # c_length = c_bottom[1] - c_top[1]
    # e_length = e_bottom[1] - e_top[1]
    #
    # cv2.line(img, c_top, c_bottom, (255, 0, 0), thickness=2)
    # cv2.putText(img, str(c_length), (c_top[0] + 10, c_top[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    #
    # cv2.line(img, e_top, e_bottom, (255, 0, 0), thickness=2)
    # cv2.putText(img, str(e_length), (e_top[0] + 10, e_top[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    #
    # return c_length, e_length


def main(image=None):
    """
    (x, y)
    ————————→ x
    |
    |
    |
    |
    ↓
    y

    坐标测量顺序: 从左向右，从上向下
    """
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/half_circle_1.jpg')
    else:
        receive = base64.b64decode(image)
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(receive)
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blurred = cv2.GaussianBlur(img_gray, (15, 15), 0)
    img_thresh = cv2.threshold(img_blurred, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    edges = cv2.Canny(img_thresh, 200, 400, 3)
    # cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
    # cv2.imshow("edges", edges)
    # cv2.waitKey(0)

    indices = numpy.where(edges != [0])
    coordinates = numpy.array(list(zip(indices[1], indices[0])))

    a_right_x, a_length = a_measurement(coordinates, img)
    b_max_length, b_min_length, b_mean_length, c_max_length, c_min_length, c_mean_length = \
        b_c_measurement(coordinates, img, a_right_x)
    # c_length, e_length = c_e_measurement(coordinates, img, distance, a_right_x)

    data = {'A': a_length, 'B': {'B_max': b_max_length, 'B_min': b_min_length, 'B_mean': b_mean_length},
            'C': {'C_max': c_max_length, 'C_min': c_min_length, 'C_mean': c_mean_length}}

    result_name = uuid.uuid1()
    cv2.imwrite('measurement/images/{}.jpg'.format(result_name), img)
    with open('measurement/images/{}.jpg'.format(result_name), 'rb') as f:
        base64_img = base64.b64encode(f.read())
    data.update({'image': base64_img})

    if os.path.exists('measurement/images/{}.jpg'.format(img_name)):
        os.remove('measurement/images/{}.jpg'.format(img_name))
    if os.path.exists('measurement/images/{}.jpg'.format(result_name)):
        os.remove('measurement/images/{}.jpg'.format(result_name))

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return data


if __name__ == '__main__':
    main()
