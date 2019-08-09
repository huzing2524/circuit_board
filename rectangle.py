# -*- coding: utf-8 -*-
# @Time   : 19-8-8 下午3:31
# @Author : huziying
# @File   : rectangle.py

# 正常不规则形状 矩形: 噪点非常多

import cv2
import numpy

numpy.set_printoptions(threshold=numpy.inf)


def a_b_measurement(coordinates, img):
    """上 左边 a点, 上 右边 b点"""
    left = coordinates[coordinates.argmin(axis=0)[0]]  # 返回沿轴axis最大/小值的索引, 0代表列, 1代表行
    right = coordinates[coordinates.argmax(axis=0)[0]]
    # print('left, right', left, right)
    width = right[0] - left[0]  # 整个形状宽度

    a_x = left[0] + width // 3
    # print('a_x', a_x)
    a_coordinate = coordinates[numpy.where(coordinates[:, 0] == a_x)]
    # print(a_coordinate)
    a_coordinate_x, a_coordinate_y = a_coordinate[0], a_coordinate[-1]
    a_length = a_coordinate_y[1] - a_coordinate_x[1]
    cv2.line(img, tuple(a_coordinate_x), tuple(a_coordinate_y), (255, 0, 0), thickness=5)
    cv2.putText(img, str(a_length), (a_coordinate_x[0] + 10, a_coordinate_x[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    b_x = left[0] + width // 3 * 2
    b_coordinate = coordinates[numpy.where(coordinates[:, 0] == b_x)]
    # print(b_coordinate)
    b_coordinate_x, b_coordinate_y = b_coordinate[0], b_coordinate[-1]
    b_length = b_coordinate_y[1] - b_coordinate_x[1]
    cv2.line(img, tuple(b_coordinate_x), tuple(b_coordinate_y), (255, 0, 0), thickness=5)
    cv2.putText(img, str(b_length), (b_coordinate_x[0] + 10, b_coordinate_x[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)


def c_d_measurement(coordinates, img):
    """左 上边 c点, 左 下边 d点"""
    top = coordinates[coordinates.argmin(axis=0)[1]]
    bottom = coordinates[coordinates.argmax(axis=0)[1]]
    # print(top, bottom)
    height = bottom[1] - top[1]  # 整个形状高度

    c_y = top[1] + height // 3
    c_coordinate = coordinates[numpy.where(coordinates[:, 1] == c_y)]
    c_coordinate_list = c_coordinate[:, 0]
    c_temp_list = list()
    for index in range(len(c_coordinate_list)):
        if c_coordinate_list[index + 1] - c_coordinate_list[index] > 1000:
            c_temp_list.append(index)
            break
    c_coordinate_x, c_coordinate_y = c_coordinate[0], c_coordinate[c_temp_list[0]]
    c_length = c_coordinate_y[0] - c_coordinate_x[0]
    cv2.line(img, tuple(c_coordinate_x), tuple(c_coordinate_y), (255, 0, 0), thickness=5)
    cv2.putText(img, str(c_length), (c_coordinate_x[0] + 10, c_coordinate_x[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    d_y = top[1] + height // 3 * 2
    d_coordinate = coordinates[numpy.where(coordinates[:, 1] == d_y)]
    # print('d_coordinate', d_coordinate)
    d_coordinate_list = d_coordinate[:, 0]
    d_temp_list = list()
    for index in range(len(d_coordinate_list)):
        if d_coordinate_list[index + 1] - d_coordinate_list[index] > 1000:
            # print('loop', d_coordinate_list[index + 1], d_coordinate_list[index], index)
            d_temp_list.append(index)
            break
    d_coordinate_x, d_coordinate_y = d_coordinate[0], d_coordinate[d_temp_list[0]]
    d_length = d_coordinate_y[0] - d_coordinate_x[0]
    cv2.line(img, tuple(d_coordinate_x), tuple(d_coordinate_y), (255, 0, 0), thickness=5)
    cv2.putText(img, str(d_length), (d_coordinate_x[0] + 10, d_coordinate_x[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)


def main():
    img = cv2.imread('./template/rectangle.jpg')
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img_blurred = cv2.GaussianBlur(img_gray, (85, 85), 0)
    # img_blurred = cv2.GaussianBlur(img_gray, (15, 15), 0)
    img_blurred = cv2.bilateralFilter(img_gray, 0, 100, 15)
    img_thresh = cv2.threshold(img_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    edges = cv2.Canny(img_thresh, 200, 400, 3)  # shape (1944, 2592)

    # cv2.namedWindow('img_thresh', cv2.WINDOW_NORMAL)
    # cv2.imshow("img_thresh", img_thresh)
    # cv2.waitKey(0)
    #
    # cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
    # cv2.imshow("edges", edges)
    # cv2.waitKey(0)

    """
    cv2.findContours()
    contours: 类型是list，contours 中每个元素都是图像中的一个轮廓，用 numpy 中的 ndarray 表示。
              轮廓中并不是存储轮廓上所有点，而是只存储可以用直线描述轮廓的点的个数，比如一个矩形只需要 4 个顶点就可以描述轮廓。
    hierarchy: 这是一个 ndarray，其中元素个数和轮廓个数相同，每个轮廓 contours[i] 对应 4 个 hierarchy 元素 
               hierarchy[i][0] ~ hierarchy[i][3]，分别表示后一个轮廓、前一个轮廓、父轮廓、内嵌轮廓的索引编号，如果没有对应项，则该值为负数。
    """
    # contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.drawContours(img, ans, -1, (0, 0, 255), 3)
    # print(type(contours)), print(contours)
    # temp_list = [c.shape[0] for c in contours]
    # index = temp_list.index(max(temp_list))
    # max_contour = contours[index]
    # print(max_contour)
    # contours = numpy.reshape(max_contour, (max_contour.shape[0], max_contour.shape[-1]))
    # for c in contours:
    #     cv2.circle(img, tuple(c), 4, (255, 0, 0))

    """凸包 cv2.convexHull()"""
    # hull = cv2.convexHull(max_contour)
    # length = len(hull)
    # print(length)
    # for i in range(length):
    #     cv2.line(img, tuple(hull[i][0]), tuple(hull[(i + 1) % length][0]), (0, 0, 255), 2)

    # indices = numpy.where(edges != [0])
    # print('indices', indices)
    # coordinates = numpy.array(list(zip(indices[0], indices[1])))
    # print(coordinates)
    # for c in coordinates:
    #     cv2.circle(img, tuple(c), 2, (255, 0, 0))

    # ans = []
    # # todo 此循环6秒，时间有点长 edges.shape = (1944, 2592)
    # for y in range(0, edges.shape[0]):
    #     for x in range(0, edges.shape[1]):
    #         if edges[y, x] != 0:
    #             ans += [[x, y]]
    # ans = numpy.array(ans)  # shape (9297, 2)

    # 0.018883943557739258 秒
    indices = numpy.where(edges != [0])
    coordinates = numpy.array(list(zip(indices[1], indices[0])))

    a_b_measurement(coordinates, img)
    c_d_measurement(coordinates, img)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)
    cv2.waitKey(0)

    # cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
    # cv2.imshow("edges", edges)
    # cv2.waitKey(0)


if __name__ == '__main__':
    main()
