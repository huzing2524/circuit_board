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

from django.db import connection

from .utils_huziying import horizontal_measurements, vertical_measurements


def polygon_2_image_process(img):
    """图片处理过程"""
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blurred = cv2.bilateralFilter(img_gray, 0, 100, 15)
    img_thresh = cv2.threshold(img_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    edges = cv2.Canny(img_thresh, 200, 400, 3)  # shape (1536, 2048)
    indices = numpy.where(edges != [0])
    coordinates = numpy.array(list(zip(indices[1], indices[0])))
    coordinates_sort = coordinates[coordinates[:, 0].argsort(), :]
    # print('coordinates_sort', coordinates_sort)

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
        img = cv2.imread('measurement/template/polygon_2.png')
    else:
        receive = base64.b64decode(image)
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(receive)
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))

    coordinates, reference_coordinate = polygon_2_image_process(img)

    height, width, dimension = img.shape
    measurements_data, data = list(), dict()

    cursor = connection.cursor()
    cursor.execute("select top_left, bottom_right, name from templates where shape = '8' and direction = '0' "
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
        #     cv2.circle(img, tuple(c), 1, (255, 0, 255), 1)

        if len(coordinates_limit_sort) > 0:
            measurement = vertical_measurements(coordinates_limit_sort, img, name)
            if measurement:
                measurements_data.append(measurement)

    cursor.execute("select top_left, bottom_right, name from templates where shape = '8' and direction = '1' "
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
        # print('coordinates_limit_sort', coordinates_limit_sort)
        # for c in coordinates_limit_sort:
        #     cv2.circle(img, tuple(c), 1, (0, 255, 255), 1)

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

    # cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)

    # cv2.destroyAllWindows()

    return data


if __name__ == '__main__':
    main()
