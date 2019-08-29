# -*- coding: utf-8 -*-
# @Time   : 19-8-22 上午10:19
# @Author : huziying
# @File   : fiber_surface.py

import cv2
import numpy
import uuid
import base64
import os


def a_b_measurement(coordinates, img):
    """"""
    height, width, dimension = img.shape
    a_x = width // 2
    a_array = coordinates[numpy.where(coordinates[:, 0] == a_x)]
    # print("a_array", a_array)

    temp_list = list()
    for index in range(len(a_array)):
        if a_array[index + 1][1] - a_array[index][1] > 300:
            temp_list.append(index)
            break
    a_array_reverse = a_array[::-1]
    for index in range(len(a_array_reverse)):
        if (a_array_reverse[index][1] - a_array_reverse[index + 1][1] > 30) and \
                (a_array_reverse[index][1] - a_array_reverse[index + 1][1] < 200):
            temp_list.append(index + 1)
            break
    # print("temp_list", temp_list)

    a_coordinate_x, a_coordinate_y = a_array[0], a_array[temp_list[0]]
    b_coordinate_x, b_coordinate_y = a_array_reverse[temp_list[1]], a_array[-1]

    a_length = a_coordinate_y[1] - a_coordinate_x[1]
    b_length = b_coordinate_y[1] - b_coordinate_x[1]

    cv2.line(img, tuple(a_coordinate_x), tuple(a_coordinate_y), (255, 0, 0), thickness=4)
    cv2.putText(img, str(a_length), (a_coordinate_x[0] + 10, a_coordinate_x[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)
    cv2.line(img, tuple(b_coordinate_x), tuple(b_coordinate_y), (255, 0, 0), thickness=4)
    cv2.putText(img, str(b_length), (b_coordinate_x[0] + 10, b_coordinate_x[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 0, 0), 4)

    return {'a': a_length, 'b': b_length}


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/fiber_surface.jpg')
    else:
        receive = base64.b64decode(image)
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(receive)
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))

    """边缘检测: 对比度差, 上边界检测不到。 使用颜色区分"""
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_blurred = cv2.bilateralFilter(img_hsv, 9, 100, 15)

    # 青色
    lower_cyan = numpy.array([78, 43, 46])
    upper_cyan = numpy.array([99, 255, 255])

    mask = cv2.inRange(img_blurred, lower_cyan, upper_cyan)
    # res = cv2.bitwise_and(img, img, mask=mask)

    edges = cv2.Canny(mask, 200, 400, 1)

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

    # cv2.namedWindow('res', cv2.WINDOW_NORMAL)
    # cv2.imshow("res", res)
    # cv2.waitKey(0)

    # cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)

    # cv2.destroyAllWindows()

    return data


if __name__ == '__main__':
    main()
