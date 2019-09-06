# -*- coding: utf-8 -*-
# @Time   : 19-8-22 上午10:29
# @Author : huziying
# @File   : copper_surface.py

import cv2
import numpy
import uuid
import base64
import os
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
        shape： 14
    """
    # 1920 2560
    # origin_point (0, 203)
    # 裁剪地方：945 1201
    # 上方框
    # ""x"":565,""y"":907,""width"":458,""height"":162
    # "x"":1491,""y"":1095,""width"":466,""height"":143
    # template = [{'relation': [(0.220703125, -0.12552083333333333), (0.399609375, -0.04114583333333333)],
    #              'type': 0},
    #             {'relation': [(0.582421875, -0.027604166666666666), (0.764453125, 0.046875)],
    #              'type': 1}]
    cursor = connection.cursor()
    cursor.execute("select name, top_left, bottom_right, direction from templates where shape = '14';")
    target = ['name', 'top_left', 'bottom_right', 'direction']
    data = cursor.fetchall()
    result = [dict(zip(target, i)) for i in data]

    # result = list()
    # result.append({'name': '1', 'top_left': (0.220703125, -0.12552083333333333),
    #                'bottom_right': (0.399609375, -0.04114583333333333),
    #                'direction': '0'})
    # result.append({'name': '1', 'top_left': (0.582421875, -0.027604166666666666),
    #                'bottom_right': (0.764453125, 0.046875),
    #                'direction': '1'})
    return result


def measurement(coordinates, template, img):
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

    origin_point = get_origin_point(cut_coordinates)
    point_1, point_2 = template['top_left'], template['bottom_right']
    x_scale = (int(point_1[0] * width + origin_point[0]), int(point_2[0] * width + origin_point[0]))
    y_scale = (int(point_1[1] * height + origin_point[1]), int(point_2[1] * height + origin_point[1]))

    if template['direction'] == '0':
        # 上部
        coordinates = cut_coordinates[numpy.where((y_scale[0] < cut_coordinates[:, 1]) & (cut_coordinates[:, 1] <= y_scale[1]))]

        y_array = list()
        y_list = list()
        for x in range(x_scale[0], x_scale[1]):
            y_points = coordinates[numpy.where(coordinates[:, 0] == x)]
            y_array.append([[x, 0], [x, y_points[-1][1]]])
            y_list.append(int(y_points[-1][1]))

        max_length = max(y_list)
        max_length_x = y_list.index(max_length)
        max_coordinates = y_array[max_length_x]
        max_coordinates[0][1] += left_array[1][1]
        max_coordinates[-1][1] += left_array[1][1]
        max_coordinates_top, b_max_coordinates_bottom = max_coordinates[0], max_coordinates[-1]
        cv2.line(img, tuple(max_coordinates_top), tuple(b_max_coordinates_bottom), (0, 255, 0), thickness=2)
        cv2.putText(img, '{} max {}'.format(template['name'], max_length), (max_coordinates_top[0] + 10, max_coordinates_top[1] + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        min_length = min(y_list)
        min_length_x = y_list.index(min_length)
        min_coordinates = y_array[min_length_x]
        min_coordinates[0][1] += left_array[1][1]
        min_coordinates[-1][1] += left_array[1][1]
        min_coordinates_top, min_coordinates_bottom = min_coordinates[0], min_coordinates[-1]
        cv2.line(img, tuple(min_coordinates_top), tuple(min_coordinates_bottom), (0, 255, 0), thickness=2)
        cv2.putText(img, '{} min {}'.format(template['name'], min_length), (min_coordinates_top[0] - 130, min_coordinates_top[1] + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        mean_length = sum(y_list) // len(y_list)
    else:
        # 下部
        coordinates = cut_coordinates[
            numpy.where((y_scale[0] < cut_coordinates[:, 1]) & (cut_coordinates[:, 1] <= y_scale[1]))]

        y_array = list()
        y_list = list()
        for x in range(x_scale[0], x_scale[1]):
            y_points = coordinates[numpy.where(coordinates[:, 0] == x)]
            y_length = left_array[2][1] - left_array[1][1] - int(y_points[0][1])
            y_array.append([[x, y_points[-1][1]], [x, left_array[2][1] - left_array[1][1]]])
            y_list.append(y_length)

        max_length = max(y_list)
        max_length_x = y_list.index(max_length)
        max_coordinates = y_array[max_length_x]
        max_coordinates[0][1] += left_array[1][1]
        max_coordinates[-1][1] += left_array[1][1]
        max_coordinates_top, b_max_coordinates_bottom = max_coordinates[0], max_coordinates[-1]
        cv2.line(img, tuple(max_coordinates_top), tuple(b_max_coordinates_bottom), (0, 255, 0), thickness=2)
        cv2.putText(img, '{} max {}'.format(template['name'], max_length), (max_coordinates_top[0] + 10, max_coordinates_top[1] + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        min_length = min(y_list)
        min_length_x = y_list.index(min_length)
        min_coordinates = y_array[min_length_x]
        min_coordinates[0][1] += left_array[1][1]
        min_coordinates[-1][1] += left_array[1][1]
        min_coordinates_top, min_coordinates_bottom = min_coordinates[0], min_coordinates[-1]
        cv2.line(img, tuple(min_coordinates_top), tuple(min_coordinates_bottom), (0, 255, 0), thickness=2)
        cv2.putText(img, '{} min {}'.format(template['name'], min_length), (min_coordinates_top[0] - 130, min_coordinates_top[1] + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        mean_length = sum(y_list) // len(y_list)
    return {'{}_max'.format(template['name']): max_length,
            '{}_min'.format(template['name']): min_length,
            '{}_mean'.format(template['name']): mean_length}


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/copper_surface.jpg')
        # img = cv2.imread('/Users/jichengjian/工作相关/大数点/光学电路板铜厚测量/jichengjian/circuit_board/measurement/template/copper_surface.jpg')
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

    data = dict()
    data['measurements_data'] = list()
    template = get_template()
    for i in template:
        data['measurements_data'].append(measurement(coordinates, i, img))

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
