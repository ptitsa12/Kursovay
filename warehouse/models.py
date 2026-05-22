from django.db import models
from employees.models import Employee
from procurement.models import Invoice
from catalog.models import Product


class MaterialAcceptance(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.PROTECT)
    acceptance_date = models.DateField(auto_now_add=True)
    accepted_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='acceptances')

    class Meta:
        verbose_name = 'Акт приёмки'
        verbose_name_plural = 'Акты приёмки'

    def __str__(self):
        return f'Приёмка #{self.id}'


class QuantityCheck(models.Model):
    RESULT_CHOICES = [
        ('match', 'Совпадает'),
        ('mismatch', 'Расхождение'),
    ]
    acceptance = models.ForeignKey(
        MaterialAcceptance, on_delete=models.CASCADE, related_name='quantity_checks'
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    declared_quantity = models.PositiveIntegerField()
    actual_quantity = models.PositiveIntegerField()
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, blank=True)

    def save(self, *args, **kwargs):
        self.result = 'match' if self.declared_quantity == self.actual_quantity else 'mismatch'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Проверка количества'
        verbose_name_plural = 'Проверки количества'


class SerialCheck(models.Model):
    acceptance = models.ForeignKey(
        MaterialAcceptance, on_delete=models.CASCADE, related_name='serial_checks'
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    serial_number = models.CharField(max_length=100)
    is_unique = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.is_unique = not SerialCheck.objects.filter(
            acceptance=self.acceptance,
            serial_number=self.serial_number,
        ).exclude(pk=self.pk).exists()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Проверка серийного номера'
        verbose_name_plural = 'Проверки серийных номеров'


class Deviation(models.Model):
    TYPE_CHOICES = [
        ('underdelivery', 'Недовложение'),
        ('overdelivery', 'Излишек'),
        ('duplicate_sn', 'Дубликат серийного номера'),
    ]
    acceptance = models.ForeignKey(
        MaterialAcceptance, on_delete=models.CASCADE, related_name='deviations'
    )
    deviation_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    detected_by = models.ForeignKey(Employee, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Отклонение'
        verbose_name_plural = 'Отклонения'

    def __str__(self):
        return f'{self.get_deviation_type_display()} #{self.id}'
