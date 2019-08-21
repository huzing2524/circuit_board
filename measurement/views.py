from django.shortcuts import render

# Create your views here.
import base64

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .utils import half_circle, line_1, line_2, line_3, rectangle_1, rectangle_2, polygon_1, polygon_2, polygon_3, \
    polygon_4, polygon_5, polygon_6, green_oil_thickness


class Measurement(APIView):
    """接口"""

    def get(self, request):
        shape = request.query_params.get("shape")  # 形状代号
        image = request.data.get("image")  # 图片 base64 encode
        # if not all([shape, image]):
        #     return Response({"res": 1, "errmsg": "缺少参数！"}, status=status.HTTP_400_BAD_REQUEST)
        if not shape:
            return Response({"res": 1, "errmsg": "缺少参数！"}, status=status.HTTP_400_BAD_REQUEST)

        if shape == "1":
            half_circle.main(image)
        elif shape == "2":
            line_1.main(image)
        elif shape == "3":
            line_2.main(image)
        elif shape == "4":
            line_3.main(image)
        elif shape == "5":
            polygon_1.main(image)
        elif shape == "6":
            polygon_2.main(image)
        elif shape == "7":
            rectangle_1.main(image)
        elif shape == "8":
            rectangle_2.main(image)
        elif shape == "9":
            polygon_3.main(image)
        elif shape == "10":
            polygon_4.main(image)
        elif shape == "11":
            polygon_5.main(image)
        elif shape == "12":
            polygon_6.main(image)
        elif shape == "13":
            green_oil_thickness.main(image)
        else:
            return Response({"res": 1, "errmsg": "参数shape代号错误！"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_200_OK)
