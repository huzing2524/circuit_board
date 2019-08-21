# -*- coding: utf-8 -*-
# @Time   : 19-8-21 下午2:46
# @Author : huziying
# @File   : green_oil_thickness.py

import cv2
import numpy
import uuid
import base64
import os


def a_measurement(coordinates, img):
    """中间 竖直位置 a"""
    left = coordinates[coordinates.argmin(axis=0)[0]]
    right = coordinates[coordinates.argmax(axis=0)[0]]
    # print(left), print(right)
    a_x = left[0] + (right[0] - left[0]) // 2 - 100
    # print("a_x", a_x)  # 1279
    a_bottom_array = coordinates[numpy.where(coordinates[:, 0] >= a_x)]
    a_bottom_sort = a_bottom_array[a_bottom_array[:, 0].argsort(), :]
    # print("a_bottom_sort", a_bottom_sort)

    a_coordinates_array = coordinates[numpy.where(coordinates[:, 0] == a_bottom_sort[0][0])][::-1]
    # print("a_coordinates_array", a_coordinates_array)
    temp_list = list()
    for index in range(len(a_coordinates_array)):
        if a_coordinates_array[index][1] - a_coordinates_array[index + 1][1] > 60:
            temp_list.append(index + 1)
            break
    a_top, a_bottom = a_coordinates_array[temp_list[0]], a_coordinates_array[0]
    # print("a_top", a_top), print("a_bottom", a_bottom)
    cv2.line(img, tuple(a_top), tuple(a_bottom), (255, 0, 0), thickness=4)
    cv2.putText(img, str(a_bottom[1] - a_top[1]), (a_top[0] + 10, a_top[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/green_oil_thickness.jpg')
    else:
        receive = base64.b64decode(image)
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(receive)
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blurred = cv2.bilateralFilter(img_gray, 9, 75, 75)
    img_thresh = cv2.adaptiveThreshold(img_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 2)

    edges = cv2.Canny(img_thresh, 200, 400, 1)

    indices = numpy.where(edges != [0])
    coordinates = numpy.array(list(zip(indices[1], indices[0])))

    a_measurement(coordinates, img)

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
