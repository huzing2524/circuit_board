# -*- coding: utf-8 -*-
# @Time   : 19-8-9 上午9:39
# @Author : huziying
# @File   : polygon_1.py

# 正常不规则形状1

import cv2
import numpy
import uuid
import base64
import os

from django.db import connection

from .utils_huziying import horizontal_measurements, vertical_measurements

numpy.set_printoptions(threshold=numpy.inf)


# def line_equation(first_x, first_y, second_x, second_y):
#     # 一元一次线性方程一般式: ax + by + c = 0
#     a = second_y - first_y
#     b = first_x - second_x
#     c = second_x * first_y - first_x * second_y
#     return a, b, c
#
#
# def a_b_c_d_measurement(coordinates, img):
#     """上 左 左边 a点, 上 左 左边 b点, 上 右 左边 c点, 上 右 右边 d点"""
#     left = coordinates[coordinates.argmin(axis=0)[0]]  # 返回沿轴axis最大/小值的索引, 0代表列, 1代表行
#     right = coordinates[coordinates.argmax(axis=0)[0]]
#     # print('left', left, 'right', right)
#     width = right[0] - left[0]
#     a_x = left[0] + int(width / 10 * 2)
#     # print('a_x', a_x)
#     a_coordinate = coordinates[numpy.where(coordinates[:, 0] == a_x)]
#     # print('a_coordinate', a_coordinate)
#     a_coordinate_x, a_coordinate_y = a_coordinate[0], a_coordinate[-1]
#     a_length = a_coordinate_y[1] - a_coordinate_x[1]
#     cv2.line(img, tuple(a_coordinate_x), tuple(a_coordinate_y), (255, 0, 0), thickness=4)
#     cv2.putText(img, str(a_length), (a_coordinate_x[0] + 10, a_coordinate_x[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 2,
#                 (255, 0, 0), 4)
#
#     b_x = left[0] + int(width / 10 * 3)
#     b_coordinate = coordinates[numpy.where(coordinates[:, 0] == b_x)]
#     # print('b_coordinate', b_coordinate)
#     b_coordinate_list = b_coordinate[:, 1]
#     b_temp_list = list()
#     for index in range(len(b_coordinate_list)):
#         if b_coordinate_list[index + 1] - b_coordinate_list[index] > 10 and b_coordinate_list[index + 1] - \
#                 b_coordinate_list[index] < 200:
#             b_temp_list.append(index + 1)
#             break
#     b_coordinate_x, b_coordinate_y = b_coordinate[0], b_coordinate[b_temp_list[0]]
#     b_length = b_coordinate_y[1] - b_coordinate_x[1]
#     cv2.line(img, tuple(b_coordinate_x), tuple(b_coordinate_y), (255, 0, 0), thickness=4)
#     cv2.putText(img, str(b_length), (b_coordinate_x[0] + 10, b_coordinate_x[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 2,
#                 (255, 0, 0), 4)
#
#     c_x = left[0] + int(width / 10 * 6)
#     c_coordinate = coordinates[numpy.where(coordinates[:, 0] == c_x)]
#     # print('c_coordinate', c_coordinate)
#     c_coordinate_list = c_coordinate[:, 1]
#     c_temp_list = list()
#     for index in range(len(c_coordinate_list)):
#         if c_coordinate_list[index + 1] - c_coordinate_list[index] > 10 and c_coordinate_list[index + 1] - \
#                 c_coordinate_list[index] < 200:
#             c_temp_list.append(index + 1)
#             break
#     c_coordinate_x, c_coordinate_y = c_coordinate[0], c_coordinate[c_temp_list[0]]
#     c_length = c_coordinate_y[1] - c_coordinate_x[1]
#     cv2.line(img, tuple(c_coordinate_x), tuple(c_coordinate_y), (255, 0, 0), thickness=4)
#     cv2.putText(img, str(c_length), (c_coordinate_x[0] + 10, c_coordinate_x[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 2,
#                 (255, 0, 0), 4)
#
#     d_x = left[0] + int(width / 10 * 7)
#     # print('d_x', d_x)
#     d_coordinate = coordinates[numpy.where(coordinates[:, 0] == d_x)]
#     # print('d_coordinate', d_coordinate)
#     d_coordinate_x, d_coordinate_y = d_coordinate[0], d_coordinate[-1]
#     d_length = d_coordinate_y[1] - d_coordinate_x[1]
#     cv2.line(img, tuple(d_coordinate_x), tuple(d_coordinate_y), (255, 0, 0), thickness=4)
#     cv2.putText(img, str(d_length), (d_coordinate_x[0] + 10, d_coordinate_x[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 2,
#                 (255, 0, 0), 4)
#
#     return b_coordinate_y, a_length, b_length, c_length, d_length
#
#
# def e_f_g_h_measurement(coordinates, img, b_coordinate_y, k_coordinate_x):
#     """中 左上 e点, 中 右上 f点, 中 左下 g点, 中 右下 h点"""
#     # print("b_coordin/ate_y", b_coordinate_y, "k_coordinate_x", k_coordinate_x)
#     limit = coordinates[
#         numpy.where((coordinates[:, 1] >= b_coordinate_y[1]) & (coordinates[:, 1] <= k_coordinate_x[1]))]
#     middle_length = k_coordinate_x[1] - b_coordinate_y[1]
#
#     e_x = b_coordinate_y[1] + middle_length // 8
#     e_coordinate = limit[numpy.where(limit[:, 1] == e_x)]
#     # print("e_coordinate", e_coordinate)
#     e_coordinate_list = e_coordinate[:, 0]
#     e_temp_list = list()
#     for index in range(len(e_coordinate_list)):
#         if e_coordinate_list[index + 1] - e_coordinate_list[index] > 10:
#             e_temp_list.append(index + 1)
#             break
#
#     e_coordinate_x, e_coordinate_y = e_coordinate[0], e_coordinate[e_temp_list[0]]
#     e_length = e_coordinate_y[0] - e_coordinate_x[0]
#     cv2.line(img, tuple(e_coordinate_x), tuple(e_coordinate_y), (255, 0, 0), thickness=4)
#     cv2.putText(img, str(e_length), (e_coordinate_x[0] + 70, e_coordinate_x[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 2,
#                 (255, 0, 0), 4)
#
#     f_coordinate = e_coordinate[::-1]
#     # print("f_coordinate", f_coordinate)
#     f_coordinate_list = f_coordinate[:, 0]
#     f_temp_list = list()
#     for index in range(len(f_coordinate_list)):
#         if f_coordinate_list[index] - f_coordinate_list[index + 1] > 50:
#             f_temp_list.append(index)
#             break
#     f_coordinate_x, f_coordinate_y = f_coordinate[f_temp_list[0]], f_coordinate[0]
#     # print("f_coordinate_x", f_coordinate_x, "f_coordinate_y", f_coordinate_y)
#     f_length = f_coordinate_y[0] - f_coordinate_x[0]
#     cv2.line(img, tuple(f_coordinate_x), tuple(f_coordinate_y), (255, 0, 0), thickness=4)
#     cv2.putText(img, str(f_length), (f_coordinate_x[0] + 70, f_coordinate_x[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 2,
#                 (255, 0, 0), 4)
#
#     g_x = b_coordinate_y[1] + int(middle_length / 8 * 3)
#     g_coordinate = limit[numpy.where(limit[:, 1] == g_x)]
#     # print("g_coordinate", g_coordinate)
#     g_coordinate_x, g_coordinate_y = g_coordinate[0], g_coordinate[1]
#     g_length = g_coordinate_y[0] - g_coordinate_x[0]
#     cv2.line(img, tuple(g_coordinate_x), tuple(g_coordinate_y), (255, 0, 0), thickness=4)
#     cv2.putText(img, str(g_length), (g_coordinate_x[0] + 70, g_coordinate_x[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 2,
#                 (255, 0, 0), 4)
#
#     h_coordinate_x, h_coordinate_y = g_coordinate[-2], g_coordinate[-1]
#     # print("h_coordinate_x", h_coordinate_x, "h_coordinate_y", h_coordinate_y)
#     h_length = h_coordinate_y[0] - h_coordinate_x[0]
#     cv2.line(img, tuple(h_coordinate_x), tuple(h_coordinate_y), (255, 0, 0), thickness=4)
#     cv2.putText(img, str(h_length), (h_coordinate_x[0] + 70, h_coordinate_x[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 2,
#                 (255, 0, 0), 4)
#
#     return g_coordinate_y, h_coordinate_x, e_length, f_length, g_length, h_length
#
#
# def i_j_measurement(coordinates, img, g_coordinate_right, h_coordinate_left, k_coordinate_x, l_coordinate_x):
#     """中 下 竖直 i点, 中下 水平 j点"""
#     # print(g_coordinate_right, h_coordinate_left, k_coordinate_x, l_coordinate_x)
#     middle_length = h_coordinate_left[0] - g_coordinate_right[0]
#     middle_x = g_coordinate_right[0] + middle_length // 2
#     middle_point_top = coordinates[
#         numpy.where((coordinates[:, 0] == middle_x) & (coordinates[:, 1] <= k_coordinate_x[1]))][-1]
#     # print("middle_point_top", middle_point_top)
#
#     # numpy.where() 多个条件交集使用 &, 并集使用 |
#     middle_limit = coordinates[numpy.where(
#         (coordinates[:, 1] < k_coordinate_x[1] + 10) & (coordinates[:, 1] > middle_point_top[1]) &
#         (coordinates[:, 0] > k_coordinate_x[0]) & (coordinates[:, 0] < l_coordinate_x[0]))]
#
#     middle_limit_left = middle_limit[numpy.where(middle_limit[:, 0] < g_coordinate_right[0])]
#     middle_limit_left_sort = middle_limit_left[middle_limit_left[:, 0].argsort(), :]  # 按照横轴x排序
#     middle_limit_right = middle_limit[numpy.where(middle_limit[:, 0] > h_coordinate_left[0])]
#     middle_limit_right_sort = middle_limit_right[middle_limit_right[:, 0].argsort(), :][::-1]  # 右边的形状变化很大！
#     # print("middle_limit_left_sort", middle_limit_left_sort), print("middle_limit_right_sort", middle_limit_right_sort)
#
#     # 左边点 x + y 最大值, 右边点 x - y 最小值
#     left_list, right_list = list(), list()
#     for l in middle_limit_left_sort:
#         left_list.append(l[0] + l[1])
#     left_index = left_list.index(max(left_list))
#     j_left = middle_limit_left_sort[left_index]
#
#     for r in middle_limit_right_sort:
#         right_list.append(r[0] - r[1])
#     right_index = right_list.index(min(right_list))
#     j_right = middle_limit_right_sort[right_index]
#
#     # print("j_left", j_left, "j_right", j_right)
#     j_length = j_right[0] - j_left[0]
#     cv2.line(img, tuple(j_left), tuple(j_right), (255, 0, 0), 2)
#     cv2.putText(img, str(j_length), (j_left[0] + 100, j_left[1] + 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4)
#
#     a, b, c = line_equation(j_left[0], j_left[1], j_right[0], j_right[1])
#     middle_point_bottom_y = int((- a * middle_point_top[0] - c) / b)
#     i_length = middle_point_bottom_y - middle_point_top[1]
#     # print('middle_point_bottom_y', middle_point_bottom_y)
#     cv2.line(img, tuple(middle_point_top), (middle_point_top[0], middle_point_bottom_y), (255, 0, 0), thickness=4)
#     cv2.putText(img, str(i_length), (middle_point_top[0] + 10, middle_point_top[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 2,
#                 (255, 0, 0), 4)
#
#     return j_length, i_length
#
#
# def k_l_measurement(coordinates, img):
#     """下 左边 k点, 下 右边 l点"""
#     bottom = coordinates[coordinates.argmax(axis=0)[1]]  # 返回沿轴axis最大/小值的索引, 0代表列, 1代表行
#     width_coordinate = coordinates[numpy.where(coordinates[:, 0] == bottom[0])][::-1]
#     # print("bottom", bottom), print("bottom_width_coordinate", bottom_width_coordinate)
#     bottom_width_coordinate_list = width_coordinate[:, 1]
#     bottom_temp_list = list()
#     for index in range(len(width_coordinate)):
#         if bottom_width_coordinate_list[index] - bottom_width_coordinate_list[index + 1] > 10:
#             bottom_temp_list.append(index + 1)
#             break
#     # print("bottom_temp_list", bottom_temp_list)
#     bottom_width_coordinate = width_coordinate[bottom_temp_list[0]]
#
#     # 通过最下面的宽度筛选坐标
#     coordinates_limit = coordinates[
#         numpy.where((coordinates[:, 1] >= bottom_width_coordinate[1] - 10) & (coordinates[:, 1] <= bottom[1] + 10))]
#     bottom_left = coordinates_limit[coordinates_limit.argmin(axis=0)[0]]  # 返回沿轴axis最大/小值的索引, 0代表列, 1代表行
#     bottom_right = coordinates_limit[coordinates_limit.argmax(axis=0)[0]]
#     # print("bottom_left", bottom_left, "bottom_right", bottom_right)
#     bottom_length = bottom_right[0] - bottom_left[0]
#     k_x = bottom_left[0] + bottom_length // 8
#     k_coordinate = coordinates_limit[numpy.where(coordinates_limit[:, 0] == k_x)]
#     # print("k_coordinate", k_coordinate)
#     k_coordinate_x, k_coordinate_y = k_coordinate[0], k_coordinate[-1]
#     k_length = k_coordinate_y[1] - k_coordinate_x[1]
#     cv2.line(img, tuple(k_coordinate_x), tuple(k_coordinate_y), (255, 0, 0), thickness=4)
#     cv2.putText(img, str(k_length), (k_coordinate_x[0] + 10, k_coordinate_x[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 2,
#                 (255, 0, 0), 4)
#
#     l_x = bottom_left[0] + int(bottom_length / 8 * 7)
#     l_coordinate = coordinates_limit[numpy.where(coordinates_limit[:, 0] == l_x)]
#     # print("l_coordinate", l_coordinate)
#     l_coordinate_x, l_coordinate_y = l_coordinate[0], l_coordinate[-1]
#     l_length = l_coordinate_y[1] - l_coordinate_x[1]
#     cv2.line(img, tuple(l_coordinate_x), tuple(l_coordinate_y), (255, 0, 0), thickness=4)
#     cv2.putText(img, str(l_length), (l_coordinate_x[0] + 10, l_coordinate_x[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 2,
#                 (255, 0, 0), 4)
#
#     return k_coordinate_x, l_coordinate_x, k_length, l_length


def polygon_1_image_process(img):
    """图片处理过程"""
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blurred = cv2.bilateralFilter(img_gray, 0, 100, 15)
    img_thresh = cv2.threshold(img_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    edges = cv2.Canny(img_thresh, 200, 400, 3)  # shape (1536, 2048)
    indices = numpy.where(edges != [0])
    coordinates = numpy.array(list(zip(indices[1], indices[0])))
    coordinates_sort = coordinates[coordinates[:, 0].argsort(), :]
    # print('coordinates', coordinates)

    location = list()
    for index in range(coordinates_sort[0][0] + 10, coordinates_sort[-1][0] - 1, 5):
        # print('index', index)
        before_c = coordinates_sort[numpy.where(coordinates_sort[:, 0] == (index + 1))]
        before_sort = before_c[before_c[:, 1].argsort(), :][0]
        next_c = coordinates_sort[numpy.where(coordinates_sort[:, 0] == index)]
        next_sort = next_c[next_c[:, 1].argsort(), :][0]
        # print('before_sort', before_sort), print('next_sort', next_sort)
        if abs(next_sort[1] - before_sort[1]) >= 10:
            location.append(index + 1)
            break
    left = coordinates[numpy.where(coordinates[:, 0] == location[0])][0]
    right = coordinates[numpy.where((coordinates[:, 1] == left[1]) & (coordinates[:, 0] > left[0] + 5))][0]
    # print('left', left), print('right', right)
    middle_x = (right[0] - left[0]) // 2 + left[0]

    reference_coordinate = coordinates[numpy.where(coordinates[:, 0] == middle_x)][0]

    # cv2.circle(img, tuple(reference_coordinate), 4, (255, 0, 255), 4)
    # cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
    # cv2.imshow("edges", edges)
    # cv2.waitKey(0)

    return coordinates, reference_coordinate


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/polygon_1.jpg')
    else:
        receive = base64.b64decode(image)
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(receive)
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))

    coordinates, reference_coordinate = polygon_1_image_process(img)

    height, width, dimension = img.shape
    measurements_data, data = list(), dict()

    cursor = connection.cursor()
    cursor.execute("select top_left, bottom_right, name from templates where shape = '7' and direction = '0' "
                   "order by name;")
    vertical = cursor.fetchall()
    for v in vertical:
        top_left = (int(v[0][0] * width + reference_coordinate[0]), int(v[0][1] * height + reference_coordinate[1]))
        bottom_right = (int(v[1][0] * width + reference_coordinate[0]), int(v[1][1] * height + reference_coordinate[1]))
        name = v[2]
        # print('top_left', top_left, 'bottom_right', bottom_right, 'name', name)
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), thickness=1)
        coordinates_limit = coordinates[numpy.where(
            (coordinates[:, 0] >= top_left[0]) & (coordinates[:, 0] <= bottom_right[0]) &
            (coordinates[:, 1] >= top_left[1]) & (coordinates[:, 1] <= bottom_right[1]))]
        coordinates_limit_sort = coordinates_limit[coordinates_limit[:, 1].argsort(), :]
        # print('coordinates_limit_sort', coordinates_limit_sort)
        # for c in coordinates_limit_sort:
        #     cv2.circle(img, tuple(c), 1, (0, 0, 255), 1)

        if len(coordinates_limit_sort) > 0:
            measurement = vertical_measurements(coordinates_limit_sort, img, name)
            if measurement:
                measurements_data.append(measurement)

    cursor.execute("select top_left, bottom_right, name from templates where shape = '7' and direction = '1' "
                   "order by name;")
    horizontal = cursor.fetchall()
    for h in horizontal:
        top_left = (int(h[0][0] * width + reference_coordinate[0]), int(h[0][1] * height + reference_coordinate[1]))
        bottom_right = (int(h[1][0] * width + reference_coordinate[0]), int(h[1][1] * height + reference_coordinate[1]))
        name = h[2]
        # print('top_left', top_left, 'bottom_right', bottom_right)

        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), thickness=1)
        coordinates_limit = coordinates[numpy.where(
            (coordinates[:, 0] >= top_left[0]) & (coordinates[:, 0] <= bottom_right[0]) &
            (coordinates[:, 1] >= top_left[1]) & (coordinates[:, 1] <= bottom_right[1]))]
        coordinates_limit_sort = coordinates_limit[coordinates_limit[:, 0].argsort(), :]

        # for c in coordinates_limit_sort:
        #     cv2.circle(img, tuple(c), 1, (0, 0, 255), 1)

        if len(coordinates_limit_sort) > 0:
            measurement = horizontal_measurements(coordinates_limit_sort, img, name)
            if measurement:
                measurements_data.append(measurement)

    data['measurements_data'] = measurements_data

    result_name = uuid.uuid1()
    cv2.imwrite('measurement/images/{}.jpg'.format(result_name), img)
    with open('measurement/images/{}.jpg'.format(result_name), 'rb') as f:
        base64_img = base64.b64encode(f.read())
    data.update({'image': base64_img})

    if os.path.exists('measurement/images/{}.jpg'.format(img_name)):
        os.remove('measurement/images/{}.jpg'.format(img_name))
    if os.path.exists('measurement/images/{}.jpg'.format(result_name)):
        os.remove('measurement/images/{}.jpg'.format(result_name))

    # cv2.namedWindow('img_thresh', cv2.WINDOW_NORMAL)
    # cv2.imshow("img_thresh", img_thresh)
    # cv2.waitKey(0)

    # cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)

    # cv2.destroyAllWindows()

    return data


if __name__ == '__main__':
    main()
