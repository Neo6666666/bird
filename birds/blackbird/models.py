from django.db import models


class Formula(models.Model):
    since_date = models.DateField(null=True, blank=True)
    up_to_date = models.DateField(null=True, blank=True)
    tax_rate = models.FloatField(default=0.0)
    tariff = models.FloatField(default=0.0)
    is_rough = models.BooleanField(default=True)
    equasion = models.TextField(max_length=300)

    def get_formula(self):
        return self.equasion

    def get_tax(self):
        return self.tax_rate

    def get_tariff(self):
        return self.tariff
