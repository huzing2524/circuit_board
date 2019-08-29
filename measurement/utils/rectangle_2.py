# -*- coding: utf-8 -*-
# @Time   : 19-8-19 上午11:32
# @Author : huziying
# @File   : rectangle_2.py

import cv2
import numpy
import uuid
import base64
import os


def a_b_measurement(coordinates, img):
    """中间宽度 a位置, 下半部 b位置"""
    left = coordinates[coordinates.argmin(axis=0)[0]]
    right = coordinates[coordinates.argmax(axis=0)[0]]
    width = right[0] - left[0]

    a_x = left[0] + width // 2
    a_coordinate = coordinates[numpy.where(coordinates[:, 0] == a_x)]
    a_coordinate_x, a_coordinate_y = a_coordinate[0], a_coordinate[-1]
    a_length = a_coordinate_y[1] - a_coordinate_x[1]
    cv2.line(img, tuple(a_coordinate_x), tuple(a_coordinate_y), (255, 0, 0), thickness=5)
    cv2.putText(img, str(a_length), (a_coordinate_x[0] + 10, a_coordinate_x[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    search_list = list()
    for x in range(a_coordinate_x[0] + 20, right[0]):
        search = coordinates[numpy.where(coordinates[:, 0] == x)]
        if len(search) >= 3:
            search_list.append(search[-2])
            search_list.append(search[-1])
            break
    b_coordinate, b_coordinate_bottom = search_list[0], search_list[1]
    b_length = b_coordinate_bottom[1] - b_coordinate[1]
    cv2.line(img, tuple(b_coordinate), tuple(b_coordinate_bottom), (255, 0, 0), thickness=5)
    cv2.putText(img, str(b_length), (b_coordinate[0] + 10, b_coordinate[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    return {'a': a_length, 'b': b_length}


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/rectangle_2.jpg')
    else:
        receive = base64.b64decode(image)
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(receive)
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img_blurred = cv2.GaussianBlur(img_gray, (15, 15), 0)
    # img_blurred = cv2.bilateralFilter(img_gray, 0, 100, 15)
    img_thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # OTSU滤波, 自动找到一个介于两波峰之间的阈值
    # img_thresh = cv2.threshold(img_blurred, 127, 255, 0)[1]  # 简单滤波
    edges = cv2.Canny(img_thresh, 200, 400, 3)  # shape (1944, 2592)

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

    # cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
    # cv2.imshow("edges", edges)
    # cv2.waitKey(0)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)
    cv2.waitKey(0)

    cv2.destroyAllWindows()

    return data


if __name__ == '__main__':
    main()
