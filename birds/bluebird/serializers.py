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
        extra_kwargs = {'klass': {'required': False},
                        'excell_name': {'required': False},
                        'inn': {'required': False},
                        'debt': {'required': False},
                        'physical_address': {'required': False},
                        }


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
