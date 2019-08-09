# -*- coding: utf-8 -*-
# @Time   : 19-8-5 下午5:31
# @Author : huziying
# @File   : half_circle.py

# 半圆形

import cv2
import numpy

numpy.set_printoptions(threshold=numpy.inf)


def a_measurement(coordinates, img):
    """最左边点 a, 正常 半圆环型"""
    a_left = coordinates[coordinates.argmin(axis=0)[0]]  # 返回沿轴axis最大/小值的索引, 0代表列, 1代表行
    # print("最左边", a_left, type(A_left[0]), A_left[0], A_left[1])  # [74 383]
    coordinate = numpy.where((coordinates[:, 1] == a_left[1]) & (coordinates[:, 0] != a_left[0]))  # <class 'tuple'> 只取第2列的最大值, 剔除自身

    a_right = coordinates[coordinate][0]
    # print("a_right", a_right, type(a_right))

    a_length = a_right[0] - a_left[0]
    # print("a_length", a_length, type(str(a_length))) [231 383]

    cv2.line(img, tuple(a_left), tuple(a_right), (255, 0, 0), thickness=2)
    cv2.putText(img, str(a_length), (a_left[0] - 10, a_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    img_height, img_width = img.shape[0], img.shape[1]
    distance = (img_width - int(a_right[0])) // 3
    # print("distance", distance)
    return distance, a_right[0]


def b_d_measurement(coordinates, img, distance, a_right_x):
    """上 左边点 b, 下左边点 d, 正常 半圆环型"""
    b_d_x = distance + a_right_x
    # print("b_d_left_x", b_d_left_x)
    b_d_coordinate_array = coordinates[numpy.where(coordinates[:, 0] == b_d_x)]
    index = numpy.argsort(b_d_coordinate_array[:, 1])  # 排序: 按照y坐标从上到下排列
    temp = [b_d_coordinate_array[i] for i in index]
    temp_2 = list()
    # print('temp', temp, len(temp))
    for t in range(len(temp) - 1):
        # print(t), print(temp[t + 1][1], temp[t][1])
        if temp[t + 1][1] - temp[t][1] >= 5:
            temp_2.append(temp[t + 1])

    temp_2.insert(0, temp[0])
    # print('temp', temp, len(temp))
    # print('temp_2', temp_2)
    b_d_coordinate_array = numpy.array(temp_2)
    # print("b_d_coordinate_array", b_d_coordinate_array)

    b_top, b_bottom = tuple(b_d_coordinate_array[index[0]]), tuple(b_d_coordinate_array[index[1]])
    d_top, d_bottom = tuple(b_d_coordinate_array[index[2]]), tuple(b_d_coordinate_array[index[3]])
    b_length = b_bottom[1] - b_top[1]
    d_length = d_bottom[1] - d_top[1]

    cv2.line(img, b_top, b_bottom, (255, 0, 0), thickness=2)
    cv2.putText(img, str(b_length), (b_top[0] + 10, b_top[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.line(img, d_top, d_bottom, (255, 0, 0), thickness=2)
    cv2.putText(img, str(d_length), (d_top[0] + 10, d_top[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)


def c_e_measurement(coordinates, img, distance, a_right_x):
    """上 右边点 c, 下 右边点 e, 正常 半圆环型"""
    c_e_x = int(distance * 2 + a_right_x)
    c_e_coordinate_array = coordinates[numpy.where(coordinates[:, 0] == c_e_x)]
    index = numpy.argsort(c_e_coordinate_array[:, 1])  # 排序: 按照y坐标从上到下排列
    # print("c_e_coordinate_array", c_e_coordinate_array), print("index", index)
    temp = [c_e_coordinate_array[i] for i in index]
    temp_2 = list()
    for t in range(len(temp) - 1):
        # print(t), print(temp[t + 1][1], temp[t][1])
        if temp[t + 1][1] - temp[t][1] >= 5:
            temp_2.append(temp[t + 1])
    temp_2.insert(0, temp[0])
    c_e_coordinate_array = numpy.array(temp_2)

    c_top, c_bottom = tuple(c_e_coordinate_array[index[0]]), tuple(c_e_coordinate_array[index[1]])
    e_top, e_bottom = tuple(c_e_coordinate_array[index[2]]), tuple(c_e_coordinate_array[index[3]])
    b_length = c_bottom[1] - c_top[1]
    d_length = e_bottom[1] - e_top[1]

    cv2.line(img, c_top, c_bottom, (255, 0, 0), thickness=2)
    cv2.putText(img, str(b_length), (c_top[0] + 10, c_top[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.line(img, e_top, e_bottom, (255, 0, 0), thickness=2)
    cv2.putText(img, str(d_length), (e_top[0] + 10, e_top[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)


def main():
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
    img = cv2.imread('/home/dsd/Desktop/circuit_board/template/half_circle_1.jpg')
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blurred = cv2.GaussianBlur(img_gray, (15, 15), 0)
    img_thresh = cv2.threshold(img_blurred, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    edges = cv2.Canny(img_thresh, 200, 400, 3)
    # cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
    # cv2.imshow("edges", edges)
    # cv2.waitKey(0)

    indices = numpy.where(edges != [0])
    coordinates = numpy.array(list(zip(indices[1], indices[0])))

    distance, a_right_x = a_measurement(coordinates, img)
    b_d_measurement(coordinates, img, distance, a_right_x)
    c_e_measurement(coordinates, img, distance, a_right_x)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
