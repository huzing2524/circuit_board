# -*- coding: utf-8 -*-
# @Time   : 19-8-19 上午11:32
# @Author : huziying
# @File   : rectangle_2.py

import cv2
import numpy
import uuid
import base64
import os

from django.db import connection

from .utils_huziying import horizontal_measurements


def a_b_measurement(coordinates, img):
    """中间宽度 a位置, 下半部 b位置"""
    left = coordinates[coordinates.argmin(axis=0)[0]]
    right = coordinates[coordinates.argmax(axis=0)[0]]
    width = right[0] - left[0]

    a_x = left[0] + width // 2
    a_coordinate = coordinates[numpy.where(coordinates[:, 0] == a_x)]
    a_coordinate_x, a_coordinate_y = a_coordinate[0], a_coordinate[-1]
    a_length = a_coordinate_y[1] - a_coordinate_x[1]
    cv2.line(img, tuple(a_coordinate_x), tuple(a_coordinate_y), (255, 0, 0), thickness=5)
    cv2.putText(img, str(a_length), (a_coordinate_x[0] + 10, a_coordinate_x[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    search_list = list()
    for x in range(a_coordinate_x[0] + 20, right[0]):
        search = coordinates[numpy.where(coordinates[:, 0] == x)]
        if len(search) >= 3:
            search_list.append(search[-2])
            search_list.append(search[-1])
            break
    b_coordinate, b_coordinate_bottom = search_list[0], search_list[1]
    b_length = b_coordinate_bottom[1] - b_coordinate[1]
    cv2.line(img, tuple(b_coordinate), tuple(b_coordinate_bottom), (255, 0, 0), thickness=5)
    cv2.putText(img, str(b_length), (b_coordinate[0] + 10, b_coordinate[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    return {'a': a_length, 'b': b_length}


def rectangle_2_image_process(img):
    """图片处理过程"""
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # OTSU滤波, 自动找到一个介于两波峰之间的阈值
    edges = cv2.Canny(img_thresh, 200, 400, 3)  # shape (1944, 2592)
    indices = numpy.where(edges != [0])
    coordinates = numpy.array(list(zip(indices[1], indices[0])))

    bottom = coordinates[coordinates.argmax(axis=0)[1]]
    top = coordinates[numpy.where(coordinates[:, 0] == bottom[0])][0]
    coordinates_limit = coordinates[numpy.where(
        (coordinates[:, 1] >= top[1] - 10) & (coordinates[:, 1] <= bottom[1] + 10))]

    reference_coordinate = coordinates_limit[coordinates_limit.argmin(axis=0)[0]]
    # print('reference_coordinate', reference_coordinate)

    # cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
    # cv2.imshow("edges", edges)
    # cv2.waitKey(0)

    return coordinates, reference_coordinate


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/rectangle_2.jpg')
    else:
        receive = base64.b64decode(image)
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(receive)
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))

    height, width, dimension = img.shape
    measurements_data, data = list(), dict()

    coordinates, reference_coordinate = rectangle_2_image_process(img)

    cursor = connection.cursor()
    cursor.execute("select top_left, bottom_right, name from templates where shape = '3' and direction = '1' "
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

    # cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)

    # cv2.destroyAllWindows()

    return data


if __name__ == '__main__':
    main()
