# -*- coding: utf-8 -*-
# @Time   : 19-8-9 上午9:39
# @Author : huziying
# @File   : polygon_1.py

# 正常不规则形状1

import cv2
import numpy

numpy.set_printoptions(threshold=numpy.inf)


def a_b_c_d_measurement(coordinates, img):
    """上 左 左边 a点, 上 左 左边 b点, 上 右 左边 c点, 上 右 右边 d点"""
    left = coordinates[coordinates.argmin(axis=0)[0]]  # 返回沿轴axis最大/小值的索引, 0代表列, 1代表行
    right = coordinates[coordinates.argmax(axis=0)[0]]
    # print('left', left, 'right', right)
    width = right[0] - left[0]
    a_x = left[0] + int(width // 10 * 2)
    # print('a_x', a_x)
    a_coordinate = coordinates[numpy.where(coordinates[:, 0] == a_x)]
    # print('a_coordinate', a_coordinate)
    a_coordinate_x, a_coordinate_y = a_coordinate[0], a_coordinate[-1]
    a_length = a_coordinate_y[1] - a_coordinate_x[1]
    cv2.line(img, tuple(a_coordinate_x), tuple(a_coordinate_y), (255, 0, 0), thickness=4)
    cv2.putText(img, str(a_length), (a_coordinate_x[0] + 10, a_coordinate_x[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    b_x = left[0] + int(width // 10 * 3)
    b_coordinate = coordinates[numpy.where(coordinates[:, 0] == b_x)]
    # print('b_coordinate', b_coordinate)
    b_coordinate_list = b_coordinate[:, 1]
    b_temp_list = list()
    for index in range(len(b_coordinate_list)):
        if b_coordinate_list[index + 1] - b_coordinate_list[index] > 10 and b_coordinate_list[index + 1] - \
                b_coordinate_list[index] < 200:
            b_temp_list.append(index + 1)
            break
    b_coordinate_x, b_coordinate_y = b_coordinate[0], b_coordinate[b_temp_list[0]]
    b_length = b_coordinate_y[1] - b_coordinate_x[1]
    cv2.line(img, tuple(b_coordinate_x), tuple(b_coordinate_y), (255, 0, 0), thickness=4)
    cv2.putText(img, str(b_length), (b_coordinate_x[0] + 10, b_coordinate_x[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    c_x = left[0] + int(width // 10 * 6)
    c_coordinate = coordinates[numpy.where(coordinates[:, 0] == c_x)]
    # print('c_coordinate', c_coordinate)
    c_coordinate_list = c_coordinate[:, 1]
    c_temp_list = list()
    for index in range(len(c_coordinate_list)):
        if c_coordinate_list[index + 1] - c_coordinate_list[index] > 10 and c_coordinate_list[index + 1] - \
                c_coordinate_list[index] < 200:
            c_temp_list.append(index + 1)
            break
    c_coordinate_x, c_coordinate_y = c_coordinate[0], c_coordinate[c_temp_list[0]]
    c_length = c_coordinate_y[1] - c_coordinate_x[1]
    cv2.line(img, tuple(c_coordinate_x), tuple(c_coordinate_y), (255, 0, 0), thickness=4)
    cv2.putText(img, str(c_length), (c_coordinate_x[0] + 10, c_coordinate_x[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)


    d_x = left[0] + int(width // 10 * 7)
    d_coordinate = coordinates[numpy.where(coordinates[:, 0] == d_x)]
    # print('d_coordinate', d_coordinate)
    d_coordinate_x, d_coordinate_y = d_coordinate[0], d_coordinate[-1]
    d_length = d_coordinate_y[1] - d_coordinate_x[1]
    cv2.line(img, tuple(d_coordinate_x), tuple(d_coordinate_y), (255, 0, 0), thickness=4)
    cv2.putText(img, str(d_length), (d_coordinate_x[0] + 10, d_coordinate_x[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)


def e_f_measurement(coordinates, img):
    """中 左上 e点, 中 右上 f点"""
    pass


def g_h_measurement(coordinates, img):
    """中 左下 g点, 中 右下 h点"""
    pass


def i_j_measurement(coordinates, img):
    """中 下 竖直 i点, 中下 水平 j点"""
    pass


def k_l_measurement(coordinates, img):
    """下 左边 k点, 下 右边 l点"""
    pass


def main():
    img = cv2.imread('./template/polygon_1.jpg')
    # img = cv2.imread('/home/dsd/Desktop/circuit_board/分类（红线为检测位置)/正常不规则矩形/1565143895.png')
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blurred = cv2.bilateralFilter(img_gray, 0, 100, 15)
    # img_blurred = cv2.GaussianBlur(img_gray, (15, 15), 0)
    # img_blurred = cv2.medianBlur(img_gray, 5)

    img_thresh = cv2.threshold(img_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    edges = cv2.Canny(img_thresh, 200, 400, 3)  # shape (1536, 2048)

    indices = numpy.where(edges != [0])
    coordinates = numpy.array(list(zip(indices[1], indices[0])))
    # print('coordinates', coordinates)

    a_b_c_d_measurement(coordinates, img)

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


if __name__ == '__main__':
    main()
