# -*- coding: utf-8 -*-
# @Time   : 19-8-22 上午10:29
# @Author : huziying
# @File   : copper_surface.py

import cv2
import numpy
import uuid
import base64
import os


def a_b_measurement(coordinates, img):
    """"""
    height, width, dimension = img.shape
    left = coordinates[coordinates.argmin(axis=0)[0]]
    left_array = coordinates[numpy.where(coordinates[:, 0] == left[0])]
    # print("left_array", left_array)

    # 裁剪图片: 左上角坐标，右下角坐标
    cut_img = img[left_array[1][1]:left_array[2][1], left_array[1][0]:width]
    # cv2.namedWindow('cut_img', cv2.WINDOW_NORMAL)
    # cv2.imshow("cut_img", cut_img)
    # cv2.waitKey(0)

    cut_img_gray = cv2.cvtColor(cut_img, cv2.COLOR_BGR2GRAY)
    cut_img_blurred = cv2.bilateralFilter(cut_img_gray, 0, 100, 15)
    cut_img_thresh = cv2.threshold(cut_img_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    cut_edges = cv2.Canny(cut_img_thresh, 200, 400, 1)
    cut_indices = numpy.where(cut_edges != [0])
    cut_coordinates = numpy.array(list(zip(cut_indices[1], cut_indices[0])))
    # print("cut_coordinates", cut_coordinates)

    middle = width // 2
    middle_coordinates = cut_coordinates[numpy.where(cut_coordinates[:, 0] == middle)]
    # print("middle_coordinates", middle_coordinates)

    origin_middle_array = coordinates[numpy.where(coordinates[:, 0] == middle)]
    a_top = origin_middle_array[1]
    a_bottom = numpy.array([a_top[0], middle_coordinates[0][1] + a_top[1]])
    a_length = str(a_bottom[1] - a_top[1])
    b_bottom = origin_middle_array[2]
    b_top = numpy.array([b_bottom[0], b_bottom[1] - ((left_array[2][1] - left_array[1][1]) - middle_coordinates[1][1])])
    b_length = str(b_bottom[1] - b_top[1])
    # print("a_top", a_top, "a_bottom", a_bottom), print("b_top", b_top, "b_bottom", b_bottom)

    cv2.line(img, tuple(a_top), tuple(a_bottom), (0, 255, 0), thickness=4)
    cv2.putText(img, a_length, (a_top[0] + 10, a_top[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (0, 255, 0), 4)

    cv2.line(img, tuple(b_top), tuple(b_bottom), (0, 255, 0), thickness=4)
    cv2.putText(img, b_length, (b_top[0] + 10, b_top[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (0, 255, 0), 4)

    return {"a": a_length, "b": b_length}


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/copper_surface.jpg')
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

    a_b_measurement(coordinates, img)

    if os.path.exists('measurement/images/{}.jpg'.format(img_name)):
        os.remove('measurement/images/{}.jpg'.format(img_name))

    # cv2.namedWindow('img_thresh', cv2.WINDOW_NORMAL)
    # cv2.imshow("img_thresh", img_thresh)
    # cv2.waitKey(0)

    # cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
    # cv2.imshow("edges", edges)
    # cv2.waitKey(0)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
