# -*- coding: utf-8 -*-
# @Time   : 19-8-21 上午9:30
# @Author : huziying
# @File   : polygon_5.py

import cv2
import numpy
import uuid
import base64
import os


def a_measurement(coordinates, img):
    """右边 竖直位置 a"""
    # left = coordinates[coordinates.argmin(axis=0)[0]]
    # left_array = coordinates[numpy.where(coordinates[:, 0] == left[0] + 100)]
    # print("left_array", left_array)
    # for l in left_array:
    #     cv2.circle(img, tuple(l), 2, (0, 0, 255), 2)

    right = coordinates[coordinates.argmax(axis=0)[0]]
    a_right_array = coordinates[numpy.where(coordinates[:, 0] == right[0] - 100)]
    # print("right", right), print("a_right_array", a_right_array)
    # for a in a_right_array:
    #     cv2.circle(img, tuple(a), 2, (0, 0, 255), 2)

    temp_list, temp_list_2 = list(), list()
    for index in range(len(a_right_array) - 1):
        if a_right_array[index + 1][1] - a_right_array[index][1] > 100:
            temp_list.append(index + 1)
            break
    a_y = a_right_array[temp_list[0]][1] if temp_list else a_right_array[0][1]

    for index in range(len(a_right_array) - 1):
        if a_right_array[index + 1][1] - a_right_array[index][1] > 300:
            temp_list_2.append(index)
            break
    a_right_bottom = a_right_array[temp_list_2[0]] if temp_list_2 else a_right_array[-1]
    # print("a_y", a_y), print('temp_list_2', temp_list_2), print("a_right_bottom", a_right_bottom)

    height, width, dimension = img.shape
    bottom_array = coordinates[numpy.where(coordinates[:, 1] <= height)][::-1]
    # print("bottom_array", bottom_array[:100])
    temp_list_3 = list()
    for index in range(len(bottom_array) - 1):
        if bottom_array[index][0] - bottom_array[index + 1][0] > 300:
            temp_list_3.append(index)
            break

    bottom_left = bottom_array[temp_list_3[0]]
    # print("bottom_left", bottom_left)

    limit = coordinates[numpy.where(
        (coordinates[:, 0] > (bottom_left[0] - 50)) & (coordinates[:, 0] < (width - 100)) &
        (coordinates[:, 1] > (a_right_bottom[1] + 80)))]
    # print("limit", len(limit))
    # for l in limit:
    #     cv2.circle(img, tuple(l), 1, (255, 0, 0), 1)

    a_coordinate_bottom = limit[limit.argmin(axis=0)[1]]
    a_coordinate_top = numpy.array([a_coordinate_bottom[0], a_y])
    a_length = a_coordinate_bottom[1] - a_coordinate_top[1]
    # print("a_coordinate_bottom", a_coordinate_bottom, "a_coordinate_top", a_coordinate_top)
    cv2.line(img, tuple(a_coordinate_top), tuple(a_coordinate_bottom), (0, 255, 0), thickness=4)
    cv2.putText(img, str(a_length), (a_coordinate_top[0] + 10, a_coordinate_top[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (0, 255, 0), 4)

    b_coordinate_bottom = numpy.array([a_coordinate_bottom[0] + 100, a_coordinate_bottom[1]])
    b_coordinate_top = numpy.array([b_coordinate_bottom[0], a_right_bottom[1]])
    b_length = b_coordinate_bottom[1] - b_coordinate_top[1]
    cv2.line(img, tuple(b_coordinate_top), tuple(b_coordinate_bottom), (0, 255, 0), thickness=4)
    cv2.putText(img, str(b_length), (b_coordinate_top[0] + 10, b_coordinate_top[1] + 60), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (0, 255, 0), 4)

    c_coordinate_top = numpy.array([a_coordinate_bottom[0] + 200, a_coordinate_bottom[1]])
    # print('c_coordinate_top', c_coordinate_top)
    c_coordinate_bottom = limit[numpy.where(limit[:, 0] == c_coordinate_top[0])][0]
    # print('c_coordinate_bottom', c_coordinate_bottom)
    # c_coordinate_bottom = numpy.array([2539, 500])
    c_length = c_coordinate_bottom[1] - c_coordinate_top[1]
    # print('c_length', c_length)
    cv2.line(img, tuple(c_coordinate_top), tuple(c_coordinate_bottom), (0, 255, 0), thickness=4)
    cv2.putText(img, str(c_length), (c_coordinate_top[0] + 10, c_coordinate_top[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (0, 255, 0), 4)

    return {'a': a_length, 'b': b_length, 'c': c_length}


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/polygon_5.jpg')
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

    data = a_measurement(coordinates, img)

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

    # cv2.destroyAllWindows()

    return data


if __name__ == '__main__':
    main()
