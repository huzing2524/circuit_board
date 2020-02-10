import base64
import os
import cv2
import uuid
import numpy

from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Template

from .utils import utils_huziying
from .utils import half_circle, line_1, line_2, line_3, rectangle_1, rectangle_2, polygon_1, polygon_2, polygon_3, \
    polygon_4, polygon_5, green_oil_thickness, fiber_surface, copper_surface, circuit_surface, \
    circuit_copper_width


class Measurement(APIView):
    """接口"""

    def post(self, request):
        shape = request.query_params.get("shape")  # 形状代号
        image = request.data.get("image")  # 图片 base64 encode
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
    """添加模板 add_template
    {
    'shape': '1',
    'image': 'base64 encode',
    'data': [
        {
            'name': 'A',
            'direction': '1',
            'coordinates': [[100, 200], [100, 300]]
        },
        {
            'name': 'B',
             'direction': '0',
            'coordinates': [[500, 600], [700, 800]]
        }]
    }
    """

    def post(self, request):
        shape = request.data.get("shape")
        image = request.data.get("image")
        data = request.data.get("data")

        if not all([shape, image, data]):
            return Response({"res": 1, "errmsg": "缺少参数！"}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(data, list):
            return Response({"res": 1, "errmsg": "data参数类型错误！"}, status=status.HTTP_400_BAD_REQUEST)

        img_name = uuid.uuid1()
        with open('measurement/images/{}.jpg'.format(img_name), 'wb') as f:
            f.write(base64.b64decode(image))
        img = cv2.imread('measurement/images/{}.jpg'.format(img_name))
        height, width, dimension = img.shape

        cursor = connection.cursor()

        sql = """
        insert into
          templates (shape, name, top_left, bottom_right, direction)
        values
          ('%s', '%s', '{%s}', '{%s}', '%s');
        """

        try:
            if shape == '1':
                reference_coordinate = half_circle.half_circle_image_process(img)[1]

                for d in data:
                    if 'name' not in d or 'direction' not in d or 'coordinates' not in d:
                        return Response({"res": 1, "errmsg": "data缺少参数！"}, status=status.HTTP_400_BAD_REQUEST)
                    if d['direction'] not in ["0", "1"]:
                        return Response({"res": 1, "errmsg": "方向参数错误！"}, status=status.HTTP_400_BAD_REQUEST)
                    template_count_by_shape_and_name = Template.objects.filter(shape=shape,name=d['name']).count()
                    print("count:" + str(template_count_by_shape_and_name))
                    if template_count_by_shape_and_name >= 1:
                        return Response({"res": 1, "errmsg": "此名称已存在！"}, status=status.HTTP_400_BAD_REQUEST)
                    top_left, bottom_right = utils_huziying.find_rectangle(d['coordinates'], reference_coordinate,
                        width, height)
                    t = Template(shape=shape, name=d['name'], top_left=top_left, bottom_right=bottom_right, direction=d['direction'])
                    t.save()
                    
                return Response({"res": 0}, status=status.HTTP_200_OK)
            elif shape == '2':
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img_blurred = cv2.bilateralFilter(img_gray, 0, 100, 15)
                img_thresh = cv2.threshold(img_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                edges = cv2.Canny(img_thresh, 200, 400, 3)  # shape (1944, 2592)
                indices = numpy.where(edges != [0])
                edges_coordinates = numpy.array(list(zip(indices[1], indices[0])))

                origin_point = edges_coordinates[0]
                for i in edges_coordinates:
                    if i[0] + i[1] < origin_point[0] + origin_point[1]:
                        origin_point[0], origin_point[1] = i

                for d in data:
                    if 'name' not in d or 'direction' not in d or 'coordinates' not in d:
                        return Response({"res": 1, "errmsg": "data缺少参数！"}, status=status.HTTP_400_BAD_REQUEST)
                    if d['direction'] not in ["0", "1"]:
                        return Response({"res": 1, "errmsg": "方向参数错误！"}, status=status.HTTP_400_BAD_REQUEST)
                    cursor.execute("select count(*) from templates where shape = '%s' and name = '%s';" %
                                   (shape, d['name']))
                    name_check = cursor.fetchone()[0]
                    if name_check >= 1:
                        return Response({"res": 1, "errmsg": "此名称已存在！"}, status=status.HTTP_400_BAD_REQUEST)

                    top_left = "%s, %s" % ((d['coordinates'][0][0] - origin_point[0]) / width,
                                           (d['coordinates'][0][1] - origin_point[1]) / height)
                    bottom_right = "%s, %s" % ((d['coordinates'][1][0] - origin_point[0]) / width,
                                               (d['coordinates'][1][1] - origin_point[1]) / height)

                    cursor.execute(sql % (shape, d['name'], top_left, bottom_right, d['direction']))
                connection.commit()

                return Response({"res": 0}, status=status.HTTP_200_OK)
            elif shape == '3':
                reference_coordinate = rectangle_2.rectangle_2_image_process(img)[1]

                for d in data:
                    if 'name' not in d or 'direction' not in d or 'coordinates' not in d:
                        return Response({"res": 1, "errmsg": "data缺少参数！"}, status=status.HTTP_400_BAD_REQUEST)
                    if d['direction'] not in ["0", "1"]:
                        return Response({"res": 1, "errmsg": "方向参数错误！"}, status=status.HTTP_400_BAD_REQUEST)
                    cursor.execute("select count(*) from templates where shape = '%s' and name = '%s';" %
                                   (shape, d['name']))
                    name_check = cursor.fetchone()[0]
                    if name_check >= 1:
                        return Response({"res": 1, "errmsg": "此名称已存在！"}, status=status.HTTP_400_BAD_REQUEST)

                    top_left, bottom_right = utils_huziying.find_rectangle(d['coordinates'], reference_coordinate,
                                                                           width, height)

                    cursor.execute(sql % (shape, d['name'], top_left, bottom_right, '1'))
                connection.commit()
            elif shape == '4':
                reference_coordinate = line_1.line_1_image_process(img)[1]
                # print('reference_coordinate', reference_coordinate)
                for d in data:
                    if 'name' not in d or 'direction' not in d or 'coordinates' not in d:
                        return Response({"res": 1, "errmsg": "data缺少参数！"}, status=status.HTTP_400_BAD_REQUEST)
                    if d['direction'] not in ["0", "1"]:
                        return Response({"res": 1, "errmsg": "方向参数错误！"}, status=status.HTTP_400_BAD_REQUEST)
                    cursor.execute("select count(*) from templates where shape = '%s' and name = '%s';" %
                                   (shape, d['name']))
                    name_check = cursor.fetchone()[0]
                    if name_check >= 1:
                        return Response({"res": 1, "errmsg": "此名称已存在！"}, status=status.HTTP_400_BAD_REQUEST)

                    top_left, bottom_right = utils_huziying.find_rectangle(d['coordinates'], reference_coordinate,
                                                                           width, height)

                    cursor.execute(sql % (shape, d['name'], top_left, bottom_right, '1'))
                connection.commit()

                return Response({"res": 0}, status=status.HTTP_200_OK)
            elif shape == '5':
                reference_coordinate = line_2.line_2_image_process(img)[1]

                for d in data:
                    if 'name' not in d or 'direction' not in d or 'coordinates' not in d:
                        return Response({"res": 1, "errmsg": "data缺少参数！"}, status=status.HTTP_400_BAD_REQUEST)
                    if d['direction'] not in ["0", "1"]:
                        return Response({"res": 1, "errmsg": "方向参数错误！"}, status=status.HTTP_400_BAD_REQUEST)
                    cursor.execute("select count(*) from templates where shape = '%s' and name = '%s';" %
                                   (shape, d['name']))
                    name_check = cursor.fetchone()[0]
                    if name_check >= 1:
                        return Response({"res": 1, "errmsg": "此名称已存在！"}, status=status.HTTP_400_BAD_REQUEST)

                    top_left, bottom_right = utils_huziying.find_rectangle(d['coordinates'], reference_coordinate,
                                                                           width, height)

                    cursor.execute(sql % (shape, d['name'], top_left, bottom_right, '1'))
                connection.commit()

                return Response({"res": 0}, status=status.HTTP_200_OK)
            elif shape == '6':
                reference_coordinate = line_3.line_3_image_process(img)[1]

                for d in data:
                    if 'name' not in d or 'direction' not in d or 'coordinates' not in d:
                        return Response({"res": 1, "errmsg": "data缺少参数！"}, status=status.HTTP_400_BAD_REQUEST)
                    if d['direction'] not in ["0", "1"]:
                        return Response({"res": 1, "errmsg": "方向参数错误！"}, status=status.HTTP_400_BAD_REQUEST)
                    cursor.execute("select count(*) from templates where shape = '%s' and name = '%s';" %
                                   (shape, d['name']))
                    name_check = cursor.fetchone()[0]
                    if name_check >= 1:
                        return Response({"res": 1, "errmsg": "此名称已存在！"}, status=status.HTTP_400_BAD_REQUEST)

                    top_left, bottom_right = utils_huziying.find_rectangle(d['coordinates'], reference_coordinate,
                                                                           width, height)

                    cursor.execute(sql % (shape, d['name'], top_left, bottom_right, '1'))
                connection.commit()

                return Response({"res": 0}, status=status.HTTP_200_OK)
            elif shape == '7':
                reference_coordinate = polygon_1.polygon_1_image_process(img)[1]

                for d in data:
                    if 'name' not in d or 'direction' not in d or 'coordinates' not in d:
                        return Response({"res": 1, "errmsg": "data缺少参数！"}, status=status.HTTP_400_BAD_REQUEST)
                    if d['direction'] not in ["0", "1"]:
                        return Response({"res": 1, "errmsg": "方向参数错误！"}, status=status.HTTP_400_BAD_REQUEST)
                    cursor.execute("select count(*) from templates where shape = '%s' and name = '%s';" %
                                   (shape, d['name']))
                    name_check = cursor.fetchone()[0]
                    if name_check >= 1:
                        return Response({"res": 1, "errmsg": "此名称已存在！"}, status=status.HTTP_400_BAD_REQUEST)

                    top_left, bottom_right = utils_huziying.find_rectangle(d['coordinates'], reference_coordinate,
                                                                           width, height)

                    cursor.execute(sql % (shape, d['name'], top_left, bottom_right, d['direction']))
                connection.commit()

                return Response({"res": 0}, status=status.HTTP_200_OK)
            elif shape == '8':
                reference_coordinate = polygon_2.polygon_2_image_process(img)[1]

                for d in data:
                    if 'name' not in d or 'direction' not in d or 'coordinates' not in d:
                        return Response({"res": 1, "errmsg": "data缺少参数！"}, status=status.HTTP_400_BAD_REQUEST)
                    if d['direction'] not in ["0", "1"]:
                        return Response({"res": 1, "errmsg": "方向参数错误！"}, status=status.HTTP_400_BAD_REQUEST)
                    cursor.execute("select count(*) from templates where shape = '%s' and name = '%s';" %
                                   (shape, d['name']))
                    name_check = cursor.fetchone()[0]
                    if name_check >= 1:
                        return Response({"res": 1, "errmsg": "此名称已存在！"}, status=status.HTTP_400_BAD_REQUEST)

                    top_left, bottom_right = utils_huziying.find_rectangle(d['coordinates'], reference_coordinate,
                                                                           width, height)

                    cursor.execute(sql % (shape, d['name'], top_left, bottom_right, d['direction']))
                connection.commit()

                return Response({"res": 0}, status=status.HTTP_200_OK)
            elif shape == '12':
                img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                img_blurred = cv2.bilateralFilter(img_hsv, 9, 100, 15)

                lower_cyan = numpy.array([78, 43, 46])
                upper_cyan = numpy.array([99, 255, 255])

                mask = cv2.inRange(img_blurred, lower_cyan, upper_cyan)
                edges = cv2.Canny(mask, 200, 400, 1)

                indices = numpy.where(edges != [0])
                edge_coordinates = numpy.array(list(zip(indices[1], indices[0])))

                origin_point = edge_coordinates[0]
                for i in edge_coordinates:
                    if i[0] - i[1] < origin_point[0] - origin_point[1]:
                        origin_point[0], origin_point[1] = i

                for d in data:
                    if 'name' not in d or 'direction' not in d or 'coordinates' not in d:
                        return Response({"res": 1, "errmsg": "data缺少参数！"}, status=status.HTTP_400_BAD_REQUEST)
                    if d['direction'] not in ["0", "1"]:
                        return Response({"res": 1, "errmsg": "方向参数错误！"}, status=status.HTTP_400_BAD_REQUEST)
                    cursor.execute("select count(*) from templates where shape = '%s' and name = '%s';" %
                                   (shape, d['name']))
                    name_check = cursor.fetchone()[0]
                    if name_check >= 1:
                        return Response({"res": 1, "errmsg": "此名称已存在！"}, status=status.HTTP_400_BAD_REQUEST)

                    top_left = "%s, %s" % ((d['coordinates'][0][0] - origin_point[0]) / width,
                                           (d['coordinates'][0][1] - origin_point[1]) / height)
                    bottom_right = "%s, %s" % ((d['coordinates'][1][0] - origin_point[0]) / width,
                                               (d['coordinates'][1][1] - origin_point[1]) / height)

                    cursor.execute(sql % (shape, d['name'], top_left, bottom_right, d['direction']))
                connection.commit()

                return Response({"res": 0}, status=status.HTTP_200_OK)
            elif shape == '13':
                img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                img_blurred = cv2.bilateralFilter(img_hsv, 9, 100, 15)

                # 青色
                lower_cyan = numpy.array([78, 43, 46])
                upper_cyan = numpy.array([99, 255, 255])
                mask = cv2.inRange(img_blurred, lower_cyan, upper_cyan)

                edges = cv2.Canny(mask, 200, 400, 1)
                indices = numpy.where(edges != [0])
                edges_coordinates = numpy.array(list(zip(indices[1], indices[0])))

                origin_point = edges_coordinates[0]
                for i in edges_coordinates:
                    if i[0] + i[1] < origin_point[0] + origin_point[1]:
                        origin_point[0], origin_point[1] = i

                for d in data:
                    if 'name' not in d or 'direction' not in d or 'coordinates' not in d:
                        return Response({"res": 1, "errmsg": "data缺少参数！"}, status=status.HTTP_400_BAD_REQUEST)
                    if d['direction'] not in ["0", "1"]:
                        return Response({"res": 1, "errmsg": "方向参数错误！"}, status=status.HTTP_400_BAD_REQUEST)
                    cursor.execute("select count(*) from templates where shape = '%s' and name = '%s';" %
                                   (shape, d['name']))
                    name_check = cursor.fetchone()[0]
                    if name_check >= 1:
                        return Response({"res": 1, "errmsg": "此名称已存在！"}, status=status.HTTP_400_BAD_REQUEST)

                    top_left = "%s, %s" % ((d['coordinates'][0][0] - origin_point[0]) / width,
                                           (d['coordinates'][0][1] - origin_point[1]) / height)
                    bottom_right = "%s, %s" % ((d['coordinates'][1][0] - origin_point[0]) / width,
                                               (d['coordinates'][1][1] - origin_point[1]) / height)

                    cursor.execute(sql % (shape, d['name'], top_left, bottom_right, d['direction']))
                connection.commit()

                return Response({"res": 0}, status=status.HTTP_200_OK)
            elif shape == '14':
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img_blurred = cv2.bilateralFilter(img_gray, 0, 100, 15)
                img_thresh = cv2.threshold(img_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[
                    1]  # OTSU滤波, 自动找到一个介于两波峰之间的阈值

                edges = cv2.Canny(img_thresh, 200, 400, 1)
                indices = numpy.where(edges != [0])
                edge_coordinates = numpy.array(list(zip(indices[1], indices[0])))

                height, width, dimension = img.shape
                left = edge_coordinates[edge_coordinates.argmin(axis=0)[0]]
                left_array = edge_coordinates[numpy.where(edge_coordinates[:, 0] == left[0])]
                cut_img = img[left_array[1][1]:left_array[2][1], left_array[1][0]:width]

                cut_img_gray = cv2.cvtColor(cut_img, cv2.COLOR_BGR2GRAY)
                cut_img_blurred = cv2.bilateralFilter(cut_img_gray, 0, 100, 15)
                cut_img_thresh = cv2.threshold(cut_img_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

                cut_edges = cv2.Canny(cut_img_thresh, 200, 400, 1)
                cut_indices = numpy.where(cut_edges != [0])
                cut_coordinates = numpy.array(list(zip(cut_indices[1], cut_indices[0])))
                # print("cut_coordinates", cut_coordinates)

                origin_point = cut_coordinates[0]
                for i in cut_coordinates:
                    if i[0] - i[1] < origin_point[0] - origin_point[1]:
                        origin_point[0], origin_point[1] = i
                origin_point[1] += left_array[1][1]

                for d in data:
                    if 'name' not in d or 'direction' not in d or 'coordinates' not in d:
                        return Response({"res": 1, "errmsg": "data缺少参数！"}, status=status.HTTP_400_BAD_REQUEST)
                    if d['direction'] not in ["0", "1"]:
                        return Response({"res": 1, "errmsg": "方向参数错误！"}, status=status.HTTP_400_BAD_REQUEST)
                    cursor.execute("select count(*) from templates where shape = '%s' and name = '%s';" %
                                   (shape, d['name']))
                    name_check = cursor.fetchone()[0]
                    if name_check >= 1:
                        return Response({"res": 1, "errmsg": "此名称已存在！"}, status=status.HTTP_400_BAD_REQUEST)

                    top_left = "%s, %s" % ((d['coordinates'][0][0] - origin_point[0]) / width,
                                           (d['coordinates'][0][1] - origin_point[1]) / height)
                    bottom_right = "%s, %s" % ((d['coordinates'][1][0] - origin_point[0]) / width,
                                               (d['coordinates'][1][1] - origin_point[1]) / height)

                    cursor.execute(sql % (shape, d['name'], top_left, bottom_right, d['direction']))
                connection.commit()

                return Response({"res": 0}, status=status.HTTP_200_OK)
            else:
                return Response({"res": 1, "errmsg": "shape参数错误！"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"res": 1, "errmsg": "服务器错误！"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()
            if os.path.exists('measurement/images/{}.jpg'.format(img_name)):
                os.remove('measurement/images/{}.jpg'.format(img_name))


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
