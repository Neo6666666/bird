from django.conf import settings
from django_q.tasks import async_task, fetch_group
from rest_framework import status
from rest_framework.parsers import (FileUploadParser, MultiPartParser)
from rest_framework.response import Response
from rest_framework.views import APIView

from bluebird.models import Contragent
from bluebird.serializers import (ContragentShortSerializer,
                                  ContragentFullSerializer,
                                  TaskSerializer)
from bluebird.utils import (parse_from_file, get_data, get_object,
                            generate_documents, create_unique_id)

from blackbird.views import calculate


class ContragentsView(APIView):
    parser_class = [FileUploadParser, MultiPartParser]

    def get(self, request):
        conrtagents = Contragent.objects.all()
        serializer = ContragentShortSerializer(conrtagents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        file = request.FILES['file']
        if file:
            result = parse_from_file(file)
            group_id = create_unique_id()  # TODO add unique id generator
            for data_element in result:
                if data_element['klass'] == 1:
                    serializer = ContragentFullSerializer(data=data_element)
                    if serializer.is_valid(True):
                        serializer.save()
                        async_task(get_data, int(serializer['id'].value),
                                   group=group_id,
                                   sync=settings.DEBUG)
            return Response(group_id, status=status.HTTP_201_CREATED)
        else:
            raise FileNotFoundError('NO FILE!')


class ContragentView(APIView):

    def get(self, request, pk):
        obj = get_object(pk, Contragent)
        serializer = ContragentFullSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        obj = get_object(pk, Contragent)
        serializer = ContragentFullSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            r = calculate(since_date=serializer['contract_accept_date'].value,
                          up_to_date=serializer['current_date'].value,
                          stat_value=serializer['stat_value'].value,
                          norm_value=serializer['norm_value'].value)
            generate_documents(r)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TasksView(APIView):
    def get(self, request, group_id):
        results = fetch_group(group_id, failures=True)
        serializer = TaskSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
