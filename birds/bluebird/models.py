import datetime

from django.contrib.auth.models import User
from django.db import models


KLASS_TYPES = [
        (1, 'Юридическое лицо без договора'),
        (2, 'Юридическое лицо с договором'),
        (3, 'ИЖС без договора'),
        (4, 'ИЖС с договором'),
        (5, 'Физическое лицо'),
    ]


class Contragent(models.Model):
    klass = models.CharField(max_length=255, choices=KLASS_TYPES,
                             default=KLASS_TYPES[0][0])
    excell_name = models.CharField(max_length=255)
    dadata_name = models.CharField(max_length=255, blank=True, null=True)
    debt = models.FloatField(default=0.00)
    inn = models.BigIntegerField(blank=True, null=True)
    ogrn = models.BigIntegerField(blank=True, null=True)
    kpp = models.BigIntegerField(blank=True, null=True)

    rs = models.CharField('Р/с', max_length=255, blank=True, null=True)
    ks = models.CharField('К/с', max_length=255, blank=True, null=True)
    bank = models.CharField('Наименование банка', max_length=255, blank=True,
                            null=True)
    bik = models.CharField('БИК', max_length=255, blank=True, null=True)
    opf = models.CharField('ОПФ', max_length=255, blank=True, null=True)

    director_status = models.CharField(max_length=255, blank=True, null=True)
    director_name = models.CharField(max_length=255, blank=True, null=True)
    creation_date = models.DateField(blank=True, null=True)
    is_func = models.BooleanField(default=True)
    okved = models.CharField(max_length=255, blank=True, null=True)
    physical_address = models.CharField(max_length=255)
    legal_address = models.CharField(max_length=255, blank=True, null=True)
    norm_value = models.ForeignKey('NormativeCategory',
                                   on_delete=models.CASCADE,
                                   blank=True, null=True)
    stat_value = models.FloatField(blank=True, null=True)
    contract_accept_date = models.DateField(
        default=datetime.date.fromisoformat('2018-07-01'), blank=True,
        null=True)
    current_date = models.DateTimeField(auto_now_add=True, blank=True,
                                        null=True)
    nunber_contract = models.CharField(max_length=255, blank=True, null=True)
    current_contract_date = models.DateTimeField(blank=True, null=True)
    signed_user = models.ForeignKey(User, blank=True, null=True,
                                    on_delete=models.CASCADE,
                                    related_name='signed')
    current_user = models.ForeignKey(User, blank=True, null=True,
                                     on_delete=models.CASCADE,
                                     related_name='current')
    platform = models.IntegerField(blank=True, null=True)


class NormativeCategory(models.Model):
    name = models.CharField(max_length=255)
    normative = models.ManyToManyField('Normative', related_name='normatives')


class Normative(models.Model):
    since_date = models.DateField(null=True, blank=True)
    up_to_date = models.DateField(null=True, blank=True)
    value = models.FloatField(null=True, blank=True)
