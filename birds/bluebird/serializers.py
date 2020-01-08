from rest_framework import serializers
from .models import Contragent

from django_q.models import Task


class ContragentShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contragent
        fields = ['id', 'klass', 'excell_name',
                  'inn', 'debt', 'physical_address']


class ContragentFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contragent
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
