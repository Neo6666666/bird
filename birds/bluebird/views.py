from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_q.tasks import async_task, fetch_group
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import (FileUploadParser, JSONParser,
                                    MultiPartParser)
from rest_framework.response import Response
from rest_framework.views import APIView

from bluebird.models import Contragent
from bluebird.serializers import ContragentSerializer, TaskSerializer
from bluebird.utils import parse_from_file, get_data


class ContragentsView(APIView):
    parser_class = [FileUploadParser, MultiPartParser]

    def get(self, request):
        conrtagents = Contragent.objects.all()
        serializer = ContragentSerializer(conrtagents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @swagger_auto_schema(manual_parameters=[openapi.Parameter('f', in_=openapi.IN_FORM, type=openapi.TYPE_FILE)])
    def post(self, request, format=None):
        file = request.FILES['file']
        if file:
            result = parse_from_file(file)
            group_id = 'test_group'
            for data_element in result:
                serializer = ContragentSerializer(data=data_element)
                if serializer.is_valid(True):
                    serializer.save()
                    print(serializer['id'].value, int(serializer['id'].value))
                    async_task(get_data, 4,
                               group=group_id, sync=True)
            return Response(group_id,
                            status=status.HTTP_201_CREATED)
        else:
            raise FileNotFoundError('NO FILE!')


class TasksView(APIView):
    def get(self, request, group_id):
        results = fetch_group(group_id, failures=True)
        serializer = TaskSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
