# -*- coding: utf-8 -*-
# @Time   : 19-8-21 下午4:51
# @Author : huziying
# @File   : line_2.py

import cv2
import numpy
import uuid
import base64
import os

from django.db import connection

from .utils_huziying import horizontal_measurements


def line_2_image_process(img):
    """图片处理"""
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blurred = cv2.bilateralFilter(img_gray, 0, 100, 15)
    img_thresh = cv2.threshold(img_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # OTSU滤波, 自动找到一个介于两波峰之间的阈值

    edges = cv2.Canny(img_thresh, 200, 400, 1)

    indices = numpy.where(edges != [0])
    coordinates = numpy.array(list(zip(indices[1], indices[0])))

    left = coordinates[coordinates.argmin(axis=0)[0]]
    whole_array = coordinates[numpy.where(coordinates[:, 0] == left[0])]
    top_limit = coordinates[numpy.where(
        (coordinates[:, 1] >= whole_array[0][1] - 10) & (coordinates[:, 1] <= whole_array[1][1] + 10))]
    reference_coordinate = top_limit[top_limit.argmax(axis=0)[0]]

    return coordinates, reference_coordinate


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/line_2.jpg')
    else:
        receive = base64.b64decode(image)
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(receive)
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))

    coordinates, reference_coordinate = line_2_image_process(img)

    height, width, dimension = img.shape
    measurements_data, data = list(), dict()

    cursor = connection.cursor()
    cursor.execute("select top_left, bottom_right, name from templates where shape = '5' and direction = '1' "
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

    # cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
    # cv2.imshow("edges", edges)
    # cv2.waitKey(0)

    # cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)

    # cv2.destroyAllWindows()

    return data


if __name__ == '__main__':
    main()
