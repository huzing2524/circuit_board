# -*- coding: utf-8 -*-
# @Time   : 19-8-21 下午2:46
# @Author : huziying
# @File   : green_oil_thickness.py

import os
import cv2
import numpy
import uuid
import base64
from django.db import connection


def get_origin_point(coordinates):
    """ 左下角的点 """
    x, y = coordinates[0]
    for i in coordinates:
        if i[0] - i[1] < x - y:
            x, y = i
    return x, y


def get_template():
    """ 获取形状对应的模版，测量类型
        shape： 12
    """
    # origin_point 0, 1149
    # 1920, 2560
    # ""x"":380,""y"":964,""width"":530,""height"":237}","{}"  ""x"":390,""y"":1018,""width"":517,""height"":145}
    # ""x"":1682,""y"":977,""width"":546,""height"":240}","{}"
    # template = [[(0.1484375, -0.09635416666666667), (0.35546875, 0.027083333333333334)],
    #             [(0.65703125, -0.08958333333333333), (0.8703125, 0.035416666666666666)]]
    cursor = connection.cursor()
    cursor.execute("select name, top_left, bottom_right, direction from templates where shape = '12';")
    target = ['name', 'top_left', 'bottom_right', 'direction']
    data = cursor.fetchall()
    result = [dict(zip(target, i)) for i in data]

    # result = list()
    # result.append({'name': '1', 'top_left': (0.15234375, -0.06822916666666666),
    #                'bottom_right': (0.354296875, 0.007291666666666667),
    #                'direction': '0'})
    # result.append({'name': '2', 'top_left': (0.65703125, -0.08958333333333333),
    #                'bottom_right': (0.8703125, 0.035416666666666666),
    #                'direction': '0'})
    return result


def a_measurement(coordinates, template, img):
    """中间 竖直位置 a"""

    origin_point = get_origin_point(coordinates)

    img_size = img.shape
    point_1, point_2 = template['top_left'], template['bottom_right']
    x_scale = (int(point_1[0] * img_size[1] + origin_point[0]), int(point_2[0] * img_size[1] + origin_point[0]))
    y_scale = (int(point_1[1] * img_size[0] + origin_point[1]), int(point_2[1] * img_size[0] + origin_point[1]))

    # if template['direction'] == '0':
    # 只有竖直宽度
    coordinates = coordinates[numpy.where((y_scale[0] < coordinates[:, 1]) & (coordinates[:, 1] < y_scale[1]))]
    y_list = list()
    for x in range(x_scale[0], x_scale[1]):
        y_array = coordinates[numpy.where(coordinates[:, 0] == x)]
        if len(y_array) > 1:
            y_list.append(int(y_array[-1][1]) - int(y_array[-2][1]))
        else:
            y_list.append(-1)
    max_length = max(y_list)
    max_length_x = y_list.index(max_length) + x_scale[0]
    max_coordinates = coordinates[numpy.where(coordinates[:, 0] == max_length_x)]
    max_coordinates_top, b_max_coordinates_bottom = max_coordinates[-2], max_coordinates[-1]
    cv2.line(img, tuple(max_coordinates_top), tuple(b_max_coordinates_bottom), (255, 0, 0), thickness=2)
    cv2.putText(img, '{} max {}'.format(template['name'], max_length), (max_coordinates_top[0] + 10,
                                                                        max_coordinates_top[1] + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    min_length = min([i for i in y_list if i > 0])
    min_length_x = y_list.index(min_length) + x_scale[0]
    min_coordinates = coordinates[numpy.where(coordinates[:, 0] == min_length_x)]
    min_coordinates_top, min_coordinates_bottom = min_coordinates[-2], min_coordinates[-1]
    cv2.line(img, tuple(min_coordinates_top), tuple(min_coordinates_bottom), (255, 0, 0), thickness=2)
    cv2.putText(img, '{} min {}'.format(template['name'], min_length), (min_coordinates_top[0] - 130,
                                                                        min_coordinates_top[1] + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
    mean_length = sum(y_list) // len(y_list)

    return {'{}_max'.format(template['name']): max_length,
            '{}_min'.format(template['name']): min_length,
            '{}_mean'.format(template['name']): mean_length}


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/green_oil_thickness.jpg')
        # img = cv2.imread('/Users/jichengjian/工作相关/大数点/光学电路板铜厚测量/jichengjian/circuit_board/measurement/template/green_oil_thickness.jpg')
    else:
        receive = base64.b64decode(image)
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(receive)
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_blurred = cv2.bilateralFilter(img_hsv, 9, 100, 15)

    # 青色
    lower_cyan = numpy.array([78, 43, 46])
    upper_cyan = numpy.array([99, 255, 255])

    mask = cv2.inRange(img_blurred, lower_cyan, upper_cyan)
    res = cv2.bitwise_and(img, img, mask=mask)

    edges = cv2.Canny(mask, 200, 400, 1)

    indices = numpy.where(edges != [0])
    coordinates = numpy.array(list(zip(indices[1], indices[0])))

    template = get_template()
    data = dict()
    data['measurements_data'] = list()
    for i in template:
        data['measurements_data'].append(a_measurement(coordinates, i, img))

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
    # cv2.imshow("edges", res)
    # cv2.waitKey(0)

    # cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)

    # cv2.destroyAllWindows()

    return data


if __name__ == '__main__':
    main()
