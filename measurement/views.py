from django.shortcuts import render

# Create your views here.
import base64

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .utils import half_circle, line, rectangle_1, rectangle_2, polygon_1, polygon_2, polygon_3, polygon_4


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
            line.main(image)
        elif shape == "3":
            polygon_1.main(image)
        elif shape == "4":
            polygon_2.main(image)
        elif shape == "5":
            rectangle_1.main(image)
        elif shape == "6":
            rectangle_2.main(image)
        elif shape == "7":
            polygon_3.main(image)
        elif shape == "8":
            polygon_4.main(image)
        else:
            return Response({"res": 1, "errmsg": "参数shape代号错误！"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_200_OK)
