from django.db import models


class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True, verbose_name='Артикул')
    name = models.CharField(max_length=200, verbose_name='Наименование')
    unit = models.CharField(max_length=20, verbose_name='Ед. изм.')
    cost_code = models.CharField(max_length=30, verbose_name='Код затрат')

    class Meta:
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'

    def __str__(self):
        return self.name
