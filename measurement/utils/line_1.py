# -*- coding: utf-8 -*-
# @Time   : 19-8-12 上午9:25
# @Author : huziying
# @File   : line_1.py

import cv2
import numpy
import uuid
import base64
import os

# numpy.set_printoptions(threshold=numpy.inf)


def a_b_measurement(coordinates, img):
    """上 a点, 下 b点"""
    left = coordinates[coordinates.argmin(axis=0)[0]]  # 返回沿轴axis最大/小值的索引, 0代表列, 1代表行
    right = coordinates[coordinates.argmax(axis=0)[0]]
    # print('left', left, 'right', right)
    a_x = (right[0] - left[0]) // 2
    a_coordinate = coordinates[numpy.where(coordinates[:, 0] == a_x)]
    # print('a_coordinate', a_coordinate)
    a_coordinate_list = a_coordinate[:, 1]
    a_temp_list = list()
    for index in range(len(a_coordinate_list) - 1):
        if a_coordinate_list[index + 1] - a_coordinate_list[index] > 10:
            a_temp_list.append(index + 1)
    # print("a_temp_list", a_temp_list)
    a_coordinate_x, a_coordinate_y = a_coordinate[0], a_coordinate[a_temp_list[0]]
    a_length = a_coordinate_y[1] - a_coordinate_x[1]
    cv2.line(img, tuple(a_coordinate_x), tuple(a_coordinate_y), (255, 0, 0), thickness=4)
    cv2.putText(img, str(a_length), (a_coordinate_x[0] + 10, a_coordinate_x[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    b_coordinate_x, b_coordinate_y = a_coordinate[a_temp_list[1]], a_coordinate[a_temp_list[2]]
    b_length = b_coordinate_y[1] - b_coordinate_x[1]
    cv2.line(img, tuple(b_coordinate_x), tuple(b_coordinate_y), (255, 0, 0), thickness=4)
    cv2.putText(img, str(b_length), (b_coordinate_x[0] + 10, b_coordinate_x[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/line_1.jpg')
    else:
        receive = base64.b64decode(image)
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(receive)
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blurred = cv2.bilateralFilter(img_gray, 0, 100, 15)
    # img_blurred = cv2.GaussianBlur(img_gray, (15, 15), 0)

    img_thresh = cv2.threshold(img_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    edges = cv2.Canny(img_thresh, 200, 400, 3)  # shape (1536, 2048)

    indices = numpy.where(edges != [0])
    coordinates = numpy.array(list(zip(indices[1], indices[0])))
    # print('coordinates', coordinates)

    a_b_measurement(coordinates, img)

    if os.path.exists('measurement/images/{}.jpg'.format(img_name)):
        os.remove('measurement/images/{}.jpg'.format(img_name))

    # cv2.namedWindow('img_thresh', cv2.WINDOW_NORMAL)
    # cv2.imshow("img_thresh", img_thresh)
    # cv2.waitKey(0)
    #
    # cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
    # cv2.imshow("edges", edges)
    # cv2.waitKey(0)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
