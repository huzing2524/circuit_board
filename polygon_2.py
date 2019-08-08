# -*- coding: utf-8 -*-
# @Time   : 19-8-8 下午3:31
# @Author : huziying
# @File   : polygon_2.py

# 正常不规则形状2: 噪点非常多

import cv2
import numpy

numpy.set_printoptions(threshold=numpy.inf)


def a_b_measurement(ans, img):
    """上 左边 a点, 上 右边 b点"""
    left = ans[ans.argmin(axis=0)[0]]  # 返回沿轴axis最大/小值的索引, 0代表列, 1代表行
    right = ans[ans.argmax(axis=0)[0]]
    # print(left, right)
    width = right[0] - left[0]  # 整个形状宽度

    a_x = left[0] + width // 3
    # print('a_x', a_x)
    a_coordinate = ans[numpy.where(ans[:, 0] == a_x)]
    a_coordinate_x, a_coordinate_y = a_coordinate[0], a_coordinate[-1]
    # print(a_coordinate)
    a_length = a_coordinate_y[1] - a_coordinate_x[1]
    cv2.line(img, tuple(a_coordinate_x), tuple(a_coordinate_y), (255, 0, 0), thickness=5)
    cv2.putText(img, str(a_length), (a_coordinate_x[0] + 10, a_coordinate_x[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    b_x = left[0] + width // 3 * 2
    b_coordinate = ans[numpy.where(ans[:, 0] == b_x)]
    # print(b_coordinate)
    b_coordinate_x, b_coordinate_y = b_coordinate[0], b_coordinate[-1]
    b_length = b_coordinate_y[1] - b_coordinate_x[1]
    cv2.line(img, tuple(b_coordinate_x), tuple(b_coordinate_y), (255, 0, 0), thickness=5)
    cv2.putText(img, str(b_length), (b_coordinate_x[0] + 10, b_coordinate_x[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)


def c_d_measurement(ans, img):
    """左 上边 c点, 左 下边 d点"""
    top = ans[ans.argmin(axis=0)[1]]
    bottom = ans[ans.argmax(axis=0)[1]]
    # print(top, bottom)
    height = bottom[1] - top[1]  # 整个形状高度

    c_y = top[1] + height // 3
    c_coordinate = ans[numpy.where(ans[:, 1] == c_y)]
    # print(c_coordinate)
    c_coordinate_x, c_coordinate_y = c_coordinate[0], c_coordinate[1]
    c_length = c_coordinate_y[0] - c_coordinate_x[0]
    cv2.line(img, tuple(c_coordinate_x), tuple(c_coordinate_y), (255, 0, 0), thickness=5)
    cv2.putText(img, str(c_length), (c_coordinate_x[0] + 10, c_coordinate_x[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    d_y = top[1] + height // 3 * 2
    d_coordinate = ans[numpy.where(ans[:, 1] == d_y)]
    # print(d_coordinate)
    d_coordinate_x, d_coordinate_y = d_coordinate[0], d_coordinate[1]
    d_length = d_coordinate_y[0] - d_coordinate_x[0]
    cv2.line(img, tuple(d_coordinate_x), tuple(d_coordinate_y), (255, 0, 0), thickness=5)
    cv2.putText(img, str(d_length), (d_coordinate_x[0] + 10, d_coordinate_x[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)


def main():
    img = cv2.imread('./template/rectangle.jpg')
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blurred = cv2.GaussianBlur(img_gray, (85, 85), 0)
    # img_blurred = cv2.bilateralFilter(img_gray, 0, 100, 15)
    # img_blurred = cv2.GaussianBlur(img_gray, (5, 5), 0)
    img_thresh = cv2.threshold(img_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    edges = cv2.Canny(img_thresh, 200, 400, 3)

    cv2.namedWindow('img_thresh', cv2.WINDOW_NORMAL)
    cv2.imshow("img_thresh", img_thresh)
    cv2.waitKey(0)

    ans = []
    for y in range(0, edges.shape[0]):
        for x in range(0, edges.shape[1]):
            if edges[y, x] != 0:
                ans += [[x, y]]
    ans = numpy.array(ans)

    a_b_measurement(ans, img)
    c_d_measurement(ans, img)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)
    cv2.waitKey(0)

    # cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
    # cv2.imshow("edges", edges)
    # cv2.waitKey(0)


if __name__ == '__main__':
    main()
