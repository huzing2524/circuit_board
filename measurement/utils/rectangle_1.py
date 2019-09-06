# -*- coding: utf-8 -*-
# @Time   : 19-8-22 上午10:29
# @Author : huziying
# @File   : rectangle_1.py

import os
import cv2
import uuid
import numpy
import base64
from django.db import connection

'''
流程：
    1、从数据库中取出对应形状的全部模版
    2、开启循环，对每个模版进行测量
        测量：
            1、过滤找到轮廓，及相对坐标原点（如最左边）
            2、将查到的模版 * 图片尺寸 + 坐标原点 = 目标范围
            3、遍历范围内部求出最大值、最小值、平均值及相似位置处的值
    3、测量结束后，将结果返回

测试：
    给定模版数据，输入新图片，看返回结果
'''
'''
vgg 左上点
----------->x(width)
|
|
|
y(height)
'''


def show_image(img):
    # 设置为WINDOW_NORMAL可以任意缩放
    cv2.namedWindow('window_name', cv2.WINDOW_NORMAL)
    cv2.imshow("window_name", img)
    # 等待按键（点窗口叉号是没用的）
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_template():
    """ 获取形状对应的模版，测量类型
        shape： 2
    """
    # 上方框
    # template = [[(0.14853395061728394, -0.08590534979423868), (0.3734567901234568, 0.09619341563786009)],
    #             [(0.49344135802469136, -0.08436213991769548), (0.7762345679012346, 0.09927983539094651)]]
    # 左方框
    # template = [[(-0.08179012345679013, 0.12191358024691358), (0.13580246913580246, 0.4207818930041152)],
    #             [(-0.08680555555555555, 0.48199588477366256), (0.13194444444444445, 0.73559670781893)]]
    cursor = connection.cursor()
    cursor.execute("select name, top_left, bottom_right, direction from templates where shape = '2';")
    target = ['name', 'top_left', 'bottom_right', 'direction']
    data = cursor.fetchall()
    result = [dict(zip(target, i)) for i in data]
    # result = list()
    # result.append({'name': '1', 'top_left': (0.14853395061728394, -0.08590534979423868),
    #                'bottom_right': (0.3734567901234568, 0.09619341563786009),
    #                'direction': '0'})
    # result.append({'name': '1', 'top_left': (0.49344135802469136, -0.08436213991769548),
    #                'bottom_right': (0.7762345679012346, 0.09927983539094651),
    #                'direction': '0'})
    return result


def get_left_upper(coordinates):
    """ 获取形状左上角的点 """
    x, y = coordinates[0]
    for i in coordinates:
        if i[0] + i[1] < x + y:
            x, y = i
    return x, y


def measurement(coordinates, template, img):
    """ 获取模版对应的区域
        template: 即模版，两个点左上和右下
        img_size：图片尺寸，height, width
    """
    origin_point = get_left_upper(coordinates)

    point_1, point_2 = template['top_left'], template['bottom_right']
    img_size = img.shape
    x_scale = (int(point_1[0] * img_size[1] + origin_point[0]), int(point_2[0] * img_size[1] + origin_point[0]))
    y_scale = (int(point_1[1] * img_size[0] + origin_point[1]), int(point_2[1] * img_size[0] + origin_point[1]))
    if template['direction'] == '0':
        # 竖直宽度
        coordinates = coordinates[numpy.where((y_scale[0] < coordinates[:, 1]) & (coordinates[:, 1] < y_scale[1]))]
        y_list = list()
        for x in range(x_scale[0], x_scale[1]):
            y_array = coordinates[numpy.where(coordinates[:, 0] == x)]
            if len(y_array) > 1:
                y_list.append(int(y_array[-1][1]) - int(y_array[0][1]))

        max_length = max(y_list)
        max_length_x = y_list.index(max_length) + x_scale[0]
        max_coordinates = coordinates[numpy.where(coordinates[:, 0] == max_length_x)]
        max_coordinates_top, b_max_coordinates_bottom = max_coordinates[0], max_coordinates[1]
        cv2.line(img, tuple(max_coordinates_top), tuple(b_max_coordinates_bottom), (255, 0, 0), thickness=2)
        cv2.putText(img, '{} max {}'.format(template['name'], max_length), (max_coordinates_top[0] + 10,
                                                                            max_coordinates_top[1] + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        min_length = min(y_list)
        min_length_x = y_list.index(min_length) + x_scale[0]
        min_coordinates = coordinates[numpy.where(coordinates[:, 0] == min_length_x)]
        min_coordinates_top, min_coordinates_bottom = min_coordinates[0], min_coordinates[-1]
        cv2.line(img, tuple(min_coordinates_top), tuple(min_coordinates_bottom), (255, 0, 0), thickness=2)
        cv2.putText(img, '{} min {}'.format(template['name'], min_length), (min_coordinates_top[0] - 130,
                                                                            min_coordinates_top[1] + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        mean_length = sum(y_list) // len(y_list)
    else:
        # 水平宽度
        coordinates = coordinates[numpy.where((x_scale[0] < coordinates[:, 0]) & (coordinates[:, 0] < x_scale[1]))]
        x_list = list()
        for y in range(y_scale[0], y_scale[1]):
            x_array = coordinates[numpy.where(coordinates[:, 1] == y)]
            if len(x_array) > 1:
                x_list.append(int(x_array[-1][0]) - int(x_array[0][0]))
            else:
                x_list.append(-1)
        max_length = max(x_list)
        max_length_y = x_list.index(max_length) + y_scale[0]
        max_coordinates = coordinates[numpy.where(coordinates[:, 1] == max_length_y)]
        max_coordinates_top, max_coordinates_bottom = max_coordinates[0], max_coordinates[1]
        cv2.line(img, tuple(max_coordinates_top), tuple(max_coordinates_bottom), (255, 0, 0), thickness=2)
        cv2.putText(img, '{} max {}'.format(template['name'], max_length), (max_coordinates_top[0] + 10,
                                                                            max_coordinates_top[1] + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        min_length = min([i for i in x_list if i > 0])
        min_length_y = x_list.index(min_length) + y_scale[0]
        min_coordinates = coordinates[numpy.where(coordinates[:, 1] == min_length_y)]
        min_coordinates_top, min_coordinates_bottom = min_coordinates[0], min_coordinates[-1]
        cv2.line(img, tuple(min_coordinates_top), tuple(min_coordinates_bottom), (255, 0, 0), thickness=2)
        cv2.putText(img, '{} min {}'.format(template['name'], min_length), (min_coordinates_top[0] - 130,
                                                                            min_coordinates_top[1] + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        mean_length = sum(x_list) // len(x_list)
    return {'{}_max'.format(template['name']): max_length,
            '{}_min'.format(template['name']): min_length,
            '{}_mean'.format(template['name']): mean_length}


def main(image=None):
    img_name = uuid.uuid1()
    if not image:
        img = cv2.imread('measurement/template/rectangle_1.jpg')
        # img = cv2.imread('/Users/jichengjian/工作相关/大数点/光学电路板铜厚测量/jichengjian/circuit_board/measurement/template/rectangle_1.jpg')
    else:
        receive = base64.b64decode(image)
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(receive)
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))

    template = get_template()
    if not template:
        return {'measurements_data': [], 'image': image}

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blurred = cv2.bilateralFilter(img_gray, 0, 100, 15)
    img_thresh = cv2.threshold(img_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    edges = cv2.Canny(img_thresh, 200, 400, 3)  # shape (1944, 2592)
    indices = numpy.where(edges != [0])
    coordinates = numpy.array(list(zip(indices[1], indices[0])))
    # print(origin_point)

    data = dict()
    data['measurements_data'] = list()
    for i in template:
        measurement_data = measurement(coordinates, i, img)
        data['measurements_data'].append(measurement_data)

    result_name = uuid.uuid1()
    cv2.imwrite('measurement/images/{}.jpg'.format(result_name), img)
    with open('measurement/images/{}.jpg'.format(result_name), 'rb') as f:
        base64_img = base64.b64encode(f.read())
    data.update({'image': base64_img})

    if os.path.exists('measurement/images/{}.jpg'.format(img_name)):
        os.remove('measurement/images/{}.jpg'.format(img_name))
    if os.path.exists('measurement/images/{}.jpg'.format(result_name)):
        os.remove('measurement/images/{}.jpg'.format(result_name))
    # show_image(img)
    return data


if __name__ == '__main__':
    # template = [{"x": 681, "y": 313, "width": 583, "height": 354}, {"x": 1575, "y": 316, "width": 733, "height": 357}]
    # origin_point: 296, 480, size: 1944, 2592
    # "{""name"":""rect"",""x"":84,""y"":717,""width"":564,""height"":581}","{}"
    # "{""name"":""rect"",""x"":71,""y"":1417,""width"":567,""height"":493}","{}"
    # cv2.circle(img, origin_point, 80, (0, 255, 0), 0)
    main()