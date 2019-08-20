# -*- coding: utf-8 -*-
# @Time   : 19-8-8 上午10:45
# @Author : huziying
# @File   : match.py

import cv2

MATCH_DICT = {0: "半圆形1", 1: "半圆形2", 2: "正常不规则矩形1", 3: "正常不规则矩形2", 4: "正常不规则矩形3"}


def half_circle_1(contours_2):
    """半圆形1"""
    template = cv2.imread('./template/half_circle_1.jpg', 0)
    thresh = cv2.threshold(template, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_1 = contours[0]

    result = cv2.matchShapes(contours_1, contours_2, 1, 0)

    if result <= 1:
        cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)
        cv2.imshow("thresh", thresh)
        cv2.waitKey(0)

    return result


def half_circle_2(contours_2):
    """半圆形2"""
    template = cv2.imread('./template/half_circle_2.jpg', 0)
    thresh = cv2.threshold(template, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_1 = contours[0]

    result = cv2.matchShapes(contours_1, contours_2, 1, 0)

    if result <= 1:
        cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)
        cv2.imshow("thresh", thresh)
        cv2.waitKey(0)

    return result


def polygon_1(contours_2):
    """不规则形状1"""
    template = cv2.imread('./template/polygon_1.jpg', 0)
    thresh = cv2.threshold(template, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_1 = contours[0]

    result = cv2.matchShapes(contours_1, contours_2, 1, 0)

    if result <= 1:
        cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)
        cv2.imshow("thresh", thresh)
        cv2.waitKey(0)

    return result


def polygon_2(contours_2):
    """不规则形状2"""
    template = cv2.imread('./template/polygon_2.png', 0)
    thresh = cv2.threshold(template, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_1 = contours[0]

    result = cv2.matchShapes(contours_1, contours_2, 1, 0)

    if result <= 1:
        cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)
        cv2.imshow("thresh", thresh)
        cv2.waitKey(0)

    return result


def rectangle(contours_2):
    """矩形"""
    template = cv2.imread('./template/rectangle_1.jpg', 0)
    thresh = cv2.threshold(template, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_1 = contours[0]

    result = cv2.matchShapes(contours_1, contours_2, 1, 0)

    if result <= 1:
        cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)
        cv2.imshow("thresh", thresh)
        cv2.waitKey(0)

    return result


# def line(contours_2):
#     """双直线"""
#     template = cv2.imread('./template/line.jpg', 0)
#     thresh = cv2.threshold(template, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
#     contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     contours_1 = contours[0]
#
#     result = cv2.matchShapes(contours_1, contours_2, 1, 0)
#
#     if result <= 1:
#         cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)
#         cv2.imshow("thresh", thresh)
#         cv2.waitKey(0)
#
#     return result


def match(image=None):
    """模板匹配，区分不同的形状"""
    image = cv2.imread('./测试图/正常标准图04.jpg', 0)
    thresh2 = cv2.threshold(image, 127, 255, 0)[1]
    contours, hierarchy = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        contours_2 = contours[0]

        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.imshow("image", image)
        cv2.waitKey(0)

        result_list = list()
        result_list.append(half_circle_1(contours_2))
        result_list.append(half_circle_2(contours_2))
        # result_list.append(line(contours_2))
        result_list.append(polygon_1(contours_2))
        result_list.append(polygon_2(contours_2))
        result_list.append(rectangle(contours_2))
        print("result_list", result_list)

        cv2.destroyAllWindows()
        return MATCH_DICT[result_list.index(min(result_list))]
    else:
        return


if __name__ == '__main__':
    print(match())
