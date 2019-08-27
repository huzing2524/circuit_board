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
    a_right_array = coordinates[numpy.where(coordinates[:, 0] == right[0] - 100)]
    print("right", right), print("a_right_array", a_right_array)

    temp_list = list()
    for index in range(len(a_right_array) - 1):
        if a_right_array[index + 1][1] - a_right_array[index][1] > 70:
            temp_list.append(index + 1)
            break
    a_y = a_right_array[temp_list[0]][1] if temp_list else a_right_array[0]
    a_right_bottom = a_right_array[-1]
    print("a_y", a_y), print("a_right_bottom", a_right_bottom)

    height, width, dimension = img.shape
    bottom_array = coordinates[numpy.where(coordinates[:, 1] <= height)]
    print("bottom_array", bottom_array)
    temp_list_2 = list()
    for index in range(len(bottom_array) - 1):
        if bottom_array[index + 1][0] - bottom_array[index][0] > 200:
            temp_list_2.append(index + 1)
            break

    # todo 图片4 有点问题，模糊导致下面没有边缘
    bottom_left = bottom_array[temp_list_2[0]]
    print("bottom_left", bottom_left)

    limit = coordinates[numpy.where(
        (coordinates[:, 0] > (bottom_left[0] - 20)) & (coordinates[:, 0] < (width - 100)) &
        (coordinates[:, 1] > (a_right_bottom[1] + 50)))]
    # print("limit", limit)
    for l in limit:
        cv2.circle(img, tuple(l), 1, (0, 255, 0), 1)

    temp_list_4 = list()
    for index in range(len(limit) - 1):
        if limit[index + 1][1] - limit[index][1] > 30:
            temp_list_4.append(index + 1)
            break
    print("temp_list_4", temp_list_4)
    a_coordinate_bottom = limit[temp_list_4[0]] if temp_list_4 else limit[limit.argmin(axis=0)[1]]
    a_coordinate_top = numpy.array([a_coordinate_bottom[0], a_y])
    a_length = a_coordinate_bottom[1] - a_coordinate_top[1]
    print("a_coordinate_bottom", a_coordinate_bottom, "a_coordinate_top", a_coordinate_top)

    cv2.line(img, tuple(a_coordinate_top), tuple(a_coordinate_bottom), (255, 0, 0), thickness=4)
    cv2.putText(img, str(a_length), (a_coordinate_top[0] + 10, a_coordinate_top[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    return a_length


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/3.jpg')
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
