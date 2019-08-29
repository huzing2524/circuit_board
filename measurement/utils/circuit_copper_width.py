# -*- coding: utf-8 -*-
# @Time   : 19-8-23 下午3:58
# @Author : huziying
# @File   : circuit_copper_width.py

import cv2
import numpy
import uuid
import base64
import os

COMBINE = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z']


def a_b_measurement(coordinates, img):
    """会有多个 部分尺寸测量 整体宽度 里面的部分位置和背景噪声很像，无法识别测量"""
    bottom = coordinates[coordinates.argmax(axis=0)[1]]
    # print("bottom", bottom)
    bottom_array = coordinates[numpy.where(coordinates[:, 0] == bottom[0])]
    # print("bottom_array", bottom_array)
    width_limit = coordinates[numpy.where(
        (coordinates[:, 1] >= bottom_array[-2][1] - 100) & (coordinates[:, 1] <= bottom_array[-1][1] + 100))]
    coordinates_limit_sort = width_limit[width_limit[:, 0].argsort(), :]
    # print("coordinates_limit_sort", coordinates_limit_sort)

    count_list, middle_list, length_list = list(), list(), list()
    for index in range(len(coordinates_limit_sort) - 1):
        if coordinates_limit_sort[index + 1][0] - coordinates_limit_sort[index][0] > 50:
            count_list.append(index)
            count_list.append(index + 1)

    count_list.insert(0, 0)
    count_list.append(len(coordinates_limit_sort) - 1)
    # print("count_list", count_list)

    # 多个物体自动测量
    for index in range(len(count_list) - 1):
        x_left, x_right = coordinates_limit_sort[count_list[index]][0], coordinates_limit_sort[count_list[index + 1]][0]
        middle = x_left + (x_right - x_left) // 2
        # print("x_left", x_left, "x_right", x_right, "middle", middle)
        middle_array = width_limit[numpy.where(width_limit[:, 0] == middle)]
        # print("middle_array", middle_array)
        if len(middle_array) > 0:
            top, bottom = middle_array[0], middle_array[-1]
            length = abs(bottom[1] - top[1])
            length_list.append(length)
            cv2.line(img, tuple(top), tuple(bottom), (255, 0, 0), thickness=4)
            cv2.putText(img, str(length), (top[0] + 10, top[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4)

    return dict(zip(COMBINE, length_list))


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/circuit_copper_width.jpg')
    else:
        receive = base64.b64decode(image)
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(receive)
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blurred = cv2.bilateralFilter(img_gray, 0, 100, 15)
    img_thresh = cv2.threshold(img_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # OTSU滤波, 自动找到一个介于两波峰之间的阈值

    edges = cv2.Canny(img_thresh, 200, 400, 1)

    indices = numpy.where(edges != [0])
    coordinates = numpy.array(list(zip(indices[1], indices[0])))

    data = a_b_measurement(coordinates, img)

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
    #
    # cv2.destroyAllWindows()

    return data


if __name__ == '__main__':
    main()
