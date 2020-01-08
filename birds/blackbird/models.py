from django.db import models


class Formula(models.Model):
    since_date = models.DateField(null=True, blank=True)
    up_to_date = models.DateField(null=True, blank=True)
    # tax_rate = models.FloatField(default=0.0)
    # tariff = models.FloatField(default=0.0)
    is_rough = models.BooleanField(default=True)
    equasion = models.TextField(max_length=300)


class NormativeCategory(models.Model):
    name = models.CharField(max_length=255)
    normative = models.ManyToManyField('Normative', related_name='normatives')


class Normative(models.Model):
    since_date = models.DateField(null=True, blank=True)
    up_to_date = models.DateField(null=True, blank=True)
    value = models.FloatField(null=True, blank=True)
