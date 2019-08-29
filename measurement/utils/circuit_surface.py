# -*- coding: utf-8 -*-
# @Time   : 19-8-22 上午10:28
# @Author : huziying
# @File   : circuit_surface.py

import cv2
import numpy
import uuid
import base64
import os


def a_b_c_d_measurement(coordinates, img):
    """上 左边位置 a, 上 右边位置 b, 下 左边位置 c, 下 右边位置 d
    先裁剪出来中间的部分，然后用颜色区分检测边缘"""

    height, width, dimension = img.shape
    right = coordinates[coordinates.argmax(axis=0)[0]]
    # print("right", right)
    top_array = coordinates[numpy.where(coordinates[:, 0] == right[0] - 200)]
    top_limit = coordinates[numpy.where(
        (coordinates[:, 1] < (top_array[-1][1] + 10)) & (coordinates[:, 1] > (top_array[-1][1] - 10)))]

    top_temp_list = list()
    for index in range(len(top_limit) - 1):
        if top_limit[index + 1][0] - top_limit[index][0] > 500:
            top_temp_list.append(index + 1)
            break
    middle_limit_left = top_limit[top_temp_list[0]]

    bottom_array = coordinates[numpy.where(coordinates[:, 1] > top_array[-1][1] + 50)]
    bottom_array_top = bottom_array[bottom_array.argmin(axis=0)[1]]
    middle_limit_right = coordinates[numpy.where(
        (coordinates[:, 1] < (bottom_array_top[1] + 10)) & (coordinates[:, 1] > (bottom_array_top[1] - 10)))][-1]
    # print("middle_limit_left", middle_limit_left, "middle_limit_right", middle_limit_right)

    # 裁剪图片: 左上角坐标，右下角坐标
    cut_img = img[top_array[-1][1]:bottom_array_top[1], 0:width]

    cut_img_gray = cv2.cvtColor(cut_img, cv2.COLOR_BGR2GRAY)
    cut_img_blurred = cv2.bilateralFilter(cut_img_gray, 0, 100, 15)
    cut_img_thresh = cv2.threshold(cut_img_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    cut_edges = cv2.Canny(cut_img_thresh, 200, 400, 1)
    cut_indices = numpy.where(cut_edges != [0])
    cut_coordinates = numpy.array(list(zip(cut_indices[1], cut_indices[0])))

    a_coordinate = cut_coordinates[numpy.where(cut_coordinates[:, 0] == middle_limit_left[0])][0]
    a_real_coordinate = numpy.array([a_coordinate[0], a_coordinate[1] + middle_limit_left[1]])
    a_length = a_real_coordinate[1] - middle_limit_left[1]

    d_coordinate = cut_coordinates[numpy.where(cut_coordinates[:, 0] == middle_limit_right[0])][-1]
    d_real_coordinate = numpy.array([d_coordinate[0], top_array[-1][1] + d_coordinate[1]])
    d_length = middle_limit_right[1] - d_real_coordinate[1]
    # print("a_coordinate", a_coordinate, "d_coordinate", d_coordinate)

    cv2.line(img, tuple(middle_limit_left), tuple(a_real_coordinate), (0, 255, 0), thickness=4)
    cv2.putText(img, str(a_length), (middle_limit_left[0] + 10, middle_limit_left[1] + 50), cv2.FONT_HERSHEY_SIMPLEX,
                2, (0, 255, 0), 4)

    cv2.line(img, tuple(middle_limit_right), tuple(d_real_coordinate), (0, 255, 0), thickness=4)
    cv2.putText(img, str(d_length), (d_real_coordinate[0] + 10, d_real_coordinate[1] + 50), cv2.FONT_HERSHEY_SIMPLEX,
                2, (0, 255, 0), 4)

    middle_length = middle_limit_right[0] - middle_limit_left[0]
    b_c_coordinates = cut_coordinates[numpy.where(cut_coordinates[:, 0] == (middle_limit_left[0] + middle_length // 2))]
    # print("b_c_coordinates", b_c_coordinates)

    b_top = top_limit[numpy.where(top_limit[:, 0] == b_c_coordinates[0][0])][-1]
    b_real_bottom = numpy.array([b_c_coordinates[0][0], b_c_coordinates[0][1] + b_top[1]])
    b_length = b_real_bottom[1] - b_top[1]
    cv2.line(img, tuple(b_top), tuple(b_real_bottom), (0, 255, 0), thickness=4)
    cv2.putText(img, str(b_length), (b_top[0] + 10, b_top[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)

    c_real_top = numpy.array([b_c_coordinates[1][0], top_array[-1][1] + b_c_coordinates[1][1]])
    bottom_limit = coordinates[numpy.where(coordinates[:, 1] >= c_real_top[1] - 20)]
    c_bottom = bottom_limit[numpy.where(bottom_limit[:, 0] == c_real_top[0])][0]
    c_length = c_bottom[1] - c_real_top[1]
    cv2.line(img, tuple(c_real_top), tuple(c_bottom), (0, 255, 0), thickness=4)
    cv2.putText(img, str(c_length), (c_real_top[0] + 10, c_real_top[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (0, 255, 0), 4)

    # cv2.namedWindow('cut_img', cv2.WINDOW_NORMAL)
    # cv2.imshow("cut_img", cut_img)
    # cv2.waitKey(0)

    return {'a': a_length, 'b': b_length, 'c': c_length, 'd': d_length}


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/circuit_surface.jpg')
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

    data = a_b_c_d_measurement(coordinates, img)

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
