import os
import cv2
import uuid
import numpy

from django.shortcuts import render
from django.db import connection

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .utils import half_circle, line_1, line_2, line_3, rectangle_1, rectangle_2, polygon_1, polygon_2, polygon_3, \
    polygon_4, polygon_5, green_oil_thickness, fiber_surface, copper_surface, circuit_surface, \
    circuit_copper_width


class Measurement(APIView):
    """接口"""

    def post(self, request):
        shape = request.query_params.get("shape")  # 形状代号
        image = request.data.get("image")  # 图片 base64 encode
        # if not all([shape, image]):
        #     return Response({"res": 1, "errmsg": "缺少参数！"}, status=status.HTTP_400_BAD_REQUEST)
        if not shape:
            return Response({"res": 1, "errmsg": "缺少参数！"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if shape == "1":
                data = half_circle.main(image)
            elif shape == "2":
                data = rectangle_1.main(image)
            elif shape == "3":
                data = rectangle_2.main(image)
            elif shape == "4":
                data = line_1.main(image)
            elif shape == "5":
                data = line_2.main(image)
            elif shape == "6":
                data = line_3.main(image)
            elif shape == "7":
                data = polygon_1.main(image)
            elif shape == "8":
                data = polygon_2.main(image)
            elif shape == "9":
                data = polygon_3.main(image)
            elif shape == "10":
                data = polygon_4.main(image)
            elif shape == "11":
                data = polygon_5.main(image)
            elif shape == "12":
                data = green_oil_thickness.main(image)
            elif shape == "13":
                data = fiber_surface.main(image)
            elif shape == "14":
                data = copper_surface.main(image)
            elif shape == "15":
                data = circuit_surface.main(image)
            elif shape == "16":
                data = circuit_copper_width.main(image)
            else:
                return Response({"res": 1, "errmsg": "参数shape代号错误！"}, status=status.HTTP_400_BAD_REQUEST)

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            # print(e)
            return Response({"res": 1, "errmsg": "服务器错误！"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddTemplate(APIView):
    """添加模板 add_template"""
    def post(self, request):
        shape = request.data.get("shape")
        image = request.data.get("image")
        coordinates = request.data.get("coordinates")  # [(100, 200), (100, 300)]

        if not all([shape, image, coordinates]):
            return Response({"res": 1, "errmsg": "缺少参数！"}, status=status.HTTP_400_BAD_REQUEST)

        img_name = uuid.uuid1()
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(image)
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))
        height, width, dimension = img.shape

        cursor = connection.cursor()

        try:
            if shape == "1":
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img_blurred = cv2.GaussianBlur(img_gray, (15, 15), 0)
                img_thresh = cv2.threshold(img_blurred, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                edges = cv2.Canny(img_thresh, 200, 400, 3)
                indices = numpy.where(edges != [0])
                coordinates = numpy.array(list(zip(indices[1], indices[0])))
                left = coordinates[coordinates.argmin(axis=0)[0]]

                x_location = (coordinates[0][0] - left[0]) / width
                y_location = (coordinates[0][1] - left[1]) / height

                if abs(coordinates[1][0] - coordinates[0][0]) <= 10:  # 竖直位置
                    cursor.execute("insert into templates (shape, x_location, y_location, direction) values "
                                   "('1', '{}', '{}', '0');".format(x_location, y_location))
                elif abs(coordinates[1][1] - coordinates[0][1]) <= 10:  # 水平位置
                    cursor.execute("insert into templates (shape, x_location, y_location, direction) values "
                                   "('1', '{}', '{}', '1');".format(x_location, y_location))

                connection.commit()

                return Response({"res": 0}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"res": 1, "errmsg": "服务器错误！"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()


class DeleteTemplate(APIView):
    """删除模板 delete_template"""
    def delete(self, request):
        shape = request.data.get("shape")
        if not shape:
            return Response({"res": 1, "errmsg": "缺少参数！"}, status=status.HTTP_400_BAD_REQUEST)

        cursor = connection.cursor()

        try:
            cursor.execute("delete from templates where shape = '{}';".format(shape))
        except Exception as e:
            return Response({"res": 1, "errmsg": "服务器错误！"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()

