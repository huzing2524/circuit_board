# -*- coding: utf-8 -*-
# @Time   : 19-9-4 下午5:03
# @Author : huziying
# @File   : utils_huziying.py

import numpy
import cv2


def find_rectangle(coordinates, reference_coordinate, width, height):
    """绘制矩形框的坐标"""
    top_left = "%s, %s" % ((coordinates[0][0] - reference_coordinate[0]) / width,
                           (coordinates[0][1] - reference_coordinate[1]) / height)
    bottom_right = "%s, %s" % ((coordinates[1][0] - reference_coordinate[0]) / width,
                               (coordinates[1][1] - reference_coordinate[1]) / height)

    return top_left, bottom_right


def horizontal_measurements(coordinates, img, name):
    """垂直位置尺寸测量，按照x坐标排列"""
    width_list = list()
    # print('coordinates', coordinates)
    for x in range(coordinates[0][0], coordinates[-1][0]):
        y_array = coordinates[numpy.where(coordinates[:, 0] == x)]
        y_array_sort = y_array[y_array[:, 1].argsort(), :]
        # print('y_array_sort', y_array_sort)
        if len(y_array_sort) >= 2:
            width_list.append(abs(int(y_array_sort[-1][1]) - int(y_array_sort[0][1])))
        else:
            continue

    # print("width_list", width_list)
    if width_list:
        max_length = max(width_list)
        max_length_x = width_list.index(max_length) + coordinates[0][0]
        max_coordinates = coordinates[numpy.where(coordinates[:, 0] == max_length_x)]
        max_coordinates_sort = max_coordinates[max_coordinates[:, 1].argsort(), :]
        max_coordinates_top, max_coordinates_bottom = max_coordinates_sort[0], max_coordinates_sort[-1]
        cv2.line(img, tuple(max_coordinates_top), tuple(max_coordinates_bottom), (255, 0, 0), thickness=2)
        cv2.putText(img, '{}_max {}'.format(name, max_length),
                    (max_coordinates_top[0] + 10, max_coordinates_top[1] + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        min_length = min(width_list)
        min_length_x = width_list.index(min_length) + coordinates[0][0]
        min_coordinates = coordinates[numpy.where(coordinates[:, 0] == min_length_x)]
        min_coordinates_sort = min_coordinates[min_coordinates[:, 1].argsort(), :]
        min_coordinates_top, min_coordinates_bottom = min_coordinates_sort[0], min_coordinates_sort[-1]
        cv2.line(img, tuple(min_coordinates_top), tuple(min_coordinates_bottom), (255, 0, 0), thickness=2)
        cv2.putText(img, '{}_min {}'.format(name, min_length),
                    (min_coordinates_bottom[0] + 10, min_coordinates_bottom[1] + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        mean_length = sum(width_list) // len(width_list)

        return {'{}_max'.format(name): max_length, '{}_min'.format(name): min_length,
                '{}_mean'.format(name): mean_length}


def vertical_measurements(coordinates, img, name):
    """水平位置尺寸测量，按照y坐标排列"""
    width_list = list()
    # print('coordinates', coordinates)
    for y in range(coordinates[0][1], coordinates[-1][1]):
        x_array = coordinates[numpy.where(coordinates[:, 1] == y)]
        x_array_sort = x_array[x_array[:, 0].argsort(), :]
        if len(x_array_sort) >= 2:
            # print('x_array_sort', x_array_sort)
            width_list.append(abs(int(x_array_sort[-1][0]) - int(x_array_sort[0][0])))
        else:
            continue

    # print("width_list", width_list)
    if width_list:
        max_length = max(width_list)
        max_length_y = width_list.index(max_length) + coordinates[0][1]
        max_coordinates = coordinates[numpy.where(coordinates[:, 1] == max_length_y)]
        max_coordinates_sort = max_coordinates[max_coordinates[:, 0].argsort(), :]
        # print('max_length', max_length, 'max_length_y', max_length_y, 'max_coordinates_sort', max_coordinates_sort)
        max_coordinates_left, max_coordinates_right = max_coordinates_sort[0], max_coordinates_sort[-1]
        cv2.line(img, tuple(max_coordinates_left), tuple(max_coordinates_right), (255, 0, 0), thickness=2)
        cv2.putText(img, '{}_max {}'.format(name, max_length), (max_coordinates_left[0], max_coordinates_left[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        min_length = min(width_list)
        min_length_y = width_list.index(min_length) + coordinates[0][1]
        min_coordinates = coordinates[numpy.where(coordinates[:, 1] == min_length_y)]
        min_coordinates_sort = min_coordinates[min_coordinates[:, 0].argsort(), :]
        # print('min_coordinates_sort', min_coordinates_sort)
        min_coordinates_top, min_coordinates_bottom = min_coordinates_sort[0], min_coordinates_sort[-1]
        cv2.line(img, tuple(min_coordinates_top), tuple(min_coordinates_bottom), (255, 0, 0), thickness=2)
        cv2.putText(img, '{}_min {}'.format(name, min_length), (min_coordinates_top[0], min_coordinates_top[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        mean_length = sum(width_list) // len(width_list)

        return {'{}_max'.format(name): max_length, '{}_min'.format(name): min_length,
                '{}_mean'.format(name): mean_length}
