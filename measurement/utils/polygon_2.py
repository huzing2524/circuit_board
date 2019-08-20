# -*- coding: utf-8 -*-
# @Time   : 19-8-9 上午9:39
# @Author : huziying
# @File   : polygon_2.py

# 正常不规则形状2

import cv2
import numpy
import uuid
import base64
import os


def a_b_measurement(coordinates, img):
    """上 左边点 a, 上右边点 b"""
    left = coordinates[coordinates.argmin(axis=0)[0]]  # 返回沿轴axis最大/小值的索引, 0代表列, 1代表行
    right = coordinates[coordinates.argmax(axis=0)[0]]

    # print('left', left, 'right', right)
    width = right[0] - left[0]
    a_x = left[0] + int(width / 10 * 2)
    a_coordinate = coordinates[numpy.where(coordinates[:, 0] == a_x)]
    a_coordinate_x, a_coordinate_y = a_coordinate[0], a_coordinate[1]
    a_length = a_coordinate_y[1] - a_coordinate_x[1]
    cv2.line(img, tuple(a_coordinate_x), tuple(a_coordinate_y), (255, 0, 0), thickness=4)
    cv2.putText(img, str(a_length), (a_coordinate_x[0] + 10, a_coordinate_x[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    b_x = left[0] + int(width / 10 * 8)
    b_coordinate = coordinates[numpy.where(coordinates[:, 0] == b_x)]
    b_coordinate_x, b_coordinate_y = b_coordinate[0], b_coordinate[1]
    # print("b_coordinate_x", b_coordinate_x, "b_coordinate_y", b_coordinate_y)
    b_length = b_coordinate_y[1] - b_coordinate_x[1]
    cv2.line(img, tuple(b_coordinate_x), tuple(b_coordinate_y), (255, 0, 0), thickness=4)
    cv2.putText(img, str(b_length), (b_coordinate_x[0] + 10, b_coordinate_x[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    return a_coordinate_y


def c_d_measurement(coordinates, img, a_coordinate_y, g_coordinate_x):
    """中 左边点 c, 中 右边点 d"""
    # print("a_coordinate_y", a_coordinate_y, "g_coordinate_x", g_coordinate_x)
    limit = coordinates[numpy.where(
        (coordinates[:, 1] >= a_coordinate_y[1]) & (coordinates[:, 1] <= g_coordinate_x[1]))]
    middle_length = g_coordinate_x[1] - a_coordinate_y[1]

    c_x = a_coordinate_y[1] + middle_length // 2
    c_coordinate = limit[numpy.where(limit[:, 1] == c_x)]
    c_coordinate_list = c_coordinate[:, 0]
    c_temp_list = list()
    for index in range(len(c_coordinate_list)):
        if c_coordinate_list[index + 1] - c_coordinate_list[index] > 10:
            c_temp_list.append(index + 1)
            break
    c_coordinate_x, c_coordinate_y = c_coordinate[0], c_coordinate[c_temp_list[0]]
    c_length = c_coordinate_y[0] - c_coordinate_x[0]
    cv2.line(img, tuple(c_coordinate_x), tuple(c_coordinate_y), (255, 0, 0), thickness=4)
    cv2.putText(img, str(c_length), (c_coordinate_x[0] + 10, c_coordinate_x[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    d_coordinate = c_coordinate[::-1]
    d_coordinate_list = d_coordinate[:, 0]
    d_temp_list = list()
    for index in range(len(d_coordinate_list)):
        if d_coordinate_list[index] - d_coordinate_list[index + 1] > 50:
            d_temp_list.append(index)
            break
    d_coordinate_x, d_coordinate_y = d_coordinate[d_temp_list[0]], d_coordinate[0]
    d_length = d_coordinate_y[0] - d_coordinate_x[0]
    cv2.line(img, tuple(d_coordinate_x), tuple(d_coordinate_y), (255, 0, 0), thickness=4)
    cv2.putText(img, str(d_length), (d_coordinate_x[0] + 10, d_coordinate_x[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    return c_coordinate_y, d_coordinate_x


def e_f_measurement(coordinates, img, c_coordinate_right, d_coordinate_left, g_coordinate_x, h_coordinate_x):
    """中下 左边点 e, 中下 右边点 f"""
    middle_limit = coordinates[numpy.where(
        (coordinates[:, 1] < g_coordinate_x[1] + 10) & (coordinates[:, 1] > c_coordinate_right[1]) &
        (coordinates[:, 0] > g_coordinate_x[0]) & (coordinates[:, 0] < h_coordinate_x[0]))]
    middle_limit_left = middle_limit[numpy.where(middle_limit[:, 0] < c_coordinate_right[0])]
    middle_limit_left_sort = middle_limit_left[middle_limit_left[:, 0].argsort(), :]
    middle_limit_right = middle_limit[numpy.where(middle_limit[:, 0] > d_coordinate_left[0])]
    middle_limit_right_sort = middle_limit_right[middle_limit_right[:, 0].argsort(), :][::-1]

    left_list, right_list = list(), list()
    for l in middle_limit_left_sort:
        left_list.append(l[0] + l[1])
    left_index = left_list.index(max(left_list))
    j_left = middle_limit_left_sort[left_index]

    for r in middle_limit_right_sort:
        right_list.append(r[0] - r[1])
    right_index = right_list.index(min(right_list))
    j_right = middle_limit_right_sort[right_index]

    j_length = j_right[0] - j_left[0]
    cv2.line(img, tuple(j_left), tuple(j_right), (255, 0, 0), 2)
    cv2.putText(img, str(j_length), (j_left[0] + 100, j_left[1] + 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4)


def g_h_measurement(coordinates, img):
    """下 左边点 g, 下 右边点 h"""
    bottom = coordinates[coordinates.argmax(axis=0)[1]]  # 返回沿轴axis最大/小值的索引, 0代表列, 1代表行
    width_coordinate = coordinates[numpy.where(coordinates[:, 0] == bottom[0])][::-1]
    # print("bottom", bottom), print("bottom_width_coordinate", bottom_width_coordinate)
    bottom_width_coordinate_list = width_coordinate[:, 1]
    bottom_temp_list = list()
    for index in range(len(width_coordinate)):
        if bottom_width_coordinate_list[index] - bottom_width_coordinate_list[index + 1] > 10:
            bottom_temp_list.append(index + 1)
            break
    # print("bottom_temp_list", bottom_temp_list)
    bottom_width_coordinate = width_coordinate[bottom_temp_list[0]]

    # 通过最下面的宽度筛选坐标
    coordinates_limit = coordinates[
        numpy.where((coordinates[:, 1] >= bottom_width_coordinate[1] - 10) & (coordinates[:, 1] <= bottom[1] + 10))]
    bottom_left = coordinates_limit[coordinates_limit.argmin(axis=0)[0]]  # 返回沿轴axis最大/小值的索引, 0代表列, 1代表行
    bottom_right = coordinates_limit[coordinates_limit.argmax(axis=0)[0]]
    # print("bottom_left", bottom_left, "bottom_right", bottom_right)
    bottom_length = bottom_right[0] - bottom_left[0]
    g_x = bottom_left[0] + bottom_length // 8
    g_coordinate = coordinates_limit[numpy.where(coordinates_limit[:, 0] == g_x)]
    # print("g_coordinate", g_coordinate)
    g_coordinate_x, g_coordinate_y = g_coordinate[0], g_coordinate[-1]
    g_length = g_coordinate_y[1] - g_coordinate_x[1]
    cv2.line(img, tuple(g_coordinate_x), tuple(g_coordinate_y), (255, 0, 0), thickness=4)
    cv2.putText(img, str(g_length), (g_coordinate_x[0] + 10, g_coordinate_x[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    h_x = bottom_left[0] + int(bottom_length / 8 * 7)
    h_coordinate = coordinates_limit[numpy.where(coordinates_limit[:, 0] == h_x)]
    # print("h_coordinate", h_coordinate)
    h_coordinate_x, h_coordinate_y = h_coordinate[0], h_coordinate[-1]
    h_length = h_coordinate_y[1] - h_coordinate_x[1]
    cv2.line(img, tuple(h_coordinate_x), tuple(h_coordinate_y), (255, 0, 0), thickness=4)
    cv2.putText(img, str(h_length), (h_coordinate_x[0] + 10, h_coordinate_x[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    return g_coordinate_x, h_coordinate_x


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/polygon_2.png')
    else:
        receive = base64.b64decode(image)
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(receive)
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blurred = cv2.bilateralFilter(img_gray, 0, 100, 15)
    img_thresh = cv2.threshold(img_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    edges = cv2.Canny(img_thresh, 200, 400, 3)

    indices = numpy.where(edges != [0])
    coordinates = numpy.array(list(zip(indices[1], indices[0])))

    a_coordinate_y = a_b_measurement(coordinates, img)
    g_coordinate_x, h_coordinate_x = g_h_measurement(coordinates, img)
    c_coordinate_y, d_coordinate_x = c_d_measurement(coordinates, img, a_coordinate_y, g_coordinate_x)
    e_f_measurement(coordinates, img, c_coordinate_y, d_coordinate_x, g_coordinate_x, h_coordinate_x)

    if os.path.exists('measurement/images/{}.jpg'.format(img_name)):
        os.remove('measurement/images/{}.jpg'.format(img_name))

    cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
    cv2.imshow("edges", edges)
    cv2.waitKey(0)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
