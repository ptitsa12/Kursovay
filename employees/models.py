from django.contrib.auth.models import AbstractUser
from django.db import models


class Employee(AbstractUser):
    position = models.CharField(max_length=100, verbose_name='Должность')
    department = models.CharField(max_length=100, verbose_name='Подразделение')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'
