# -*- coding: utf-8 -*-
# @Time   : 19-8-21 上午9:30
# @Author : huziying
# @File   : polygon_6.py

import cv2
import numpy
import uuid
import base64
import os


def a_measurement(coordinates, img):
    """右边 竖直位置 a"""
    right = coordinates[coordinates.argmax(axis=0)[0]]
    a_right_array = coordinates[numpy.where(coordinates[:, 0] == right[0])]
    # print("right", right), print("a_right_array", a_right_array)
    temp_list = list()
    for index in range(len(a_right_array)):
        if a_right_array[index + 1][1] - a_right_array[index][1] > 70:
            temp_list.append(index + 1)
            break
    a_y = a_right_array[temp_list[0]]
    a_right_bottom = a_right_array[-1]
    # print("a_y", a_y), print("a_right_bottom", a_right_bottom)

    # limit = coordinates[numpy.where(coordinates[:, 1] > (a_right_bottom[1] + 70))][0]
    # print("limit", limit)

    bottom = coordinates[coordinates.argmax(axis=0)[1]]
    # print("bottom", bottom)  # [1182 1919]
    a_bottom_array = coordinates[numpy.where(coordinates[:, 1] == bottom[1] - 300)]
    # print("a_bottom_array", a_bottom_array)
    a_x_1 = 1662
    a_bottom_array_2 = coordinates[numpy.where(coordinates[:, 1] >= (bottom[1] - 600))]
    # print("a_bottom_array_2", a_bottom_array_2)
    a_x_2 = 1648

    a_bottom_array_3 = coordinates[numpy.where(coordinates[:, 1] >= (bottom[1] - 900))]
    # print("a_bottom_array_3", a_bottom_array_3)
    a_x_3 = 1640

    a_x_mean = (a_x_1 + a_x_2 + a_x_3) // 3
    print("a_x_mean", a_x_mean)

    a_coordinate_bottom = coordinates[numpy.where(coordinates[:, 0] == a_x_mean)]
    # print("a_coordinate_bottom", a_coordinate_bottom)

    cv2.line(img, (a_x_mean, 238), (a_x_mean, 518), (255, 0, 0), thickness=4)


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/polygon_6.jpg')
    else:
        receive = base64.b64decode(image)
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(receive)
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blurred = cv2.bilateralFilter(img_gray, 0, 100, 15)
    # 灰度: 白色为255, 黑色为0
    img_thresh = cv2.adaptiveThreshold(img_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    edges = cv2.Canny(img_thresh, 200, 400, 1)

    indices = numpy.where(edges != [0])
    coordinates = numpy.array(list(zip(indices[1], indices[0])))

    a_measurement(coordinates, img)

    if os.path.exists('measurement/images/{}.jpg'.format(img_name)):
        os.remove('measurement/images/{}.jpg'.format(img_name))

    cv2.namedWindow('img_thresh', cv2.WINDOW_NORMAL)
    cv2.imshow("img_thresh", img_thresh)
    cv2.waitKey(0)

    cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
    cv2.imshow("edges", edges)
    cv2.waitKey(0)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
