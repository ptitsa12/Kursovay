from django.db import models
from employees.models import Employee
from suppliers.models import Supplier
from catalog.models import Product


class PurchaseRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('accepted', 'Принята в работу'),
        ('rejected', 'Отклонена'),
        ('completed', 'Выполнена'),
    ]
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    desired_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='requests')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка на закупку'
        verbose_name_plural = 'Заявки на закупку'

    def __str__(self):
        return f'Заявка #{self.id} от {self.created_by}'


class SupplierOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('sent', 'Отправлен'),
        ('partial', 'Частично выполнен'),
        ('completed', 'Выполнен'),
    ]
    request = models.OneToOneField(PurchaseRequest, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_number = models.CharField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.order_number:
            self.order_number = f'ORD-{self.request_id}-{self.order_date.year}'
            super().save(update_fields=['order_number'])

    class Meta:
        verbose_name = 'Заказ поставщику'
        verbose_name_plural = 'Заказы поставщикам'

    def __str__(self):
        return self.order_number or f'Заказ #{self.id}'


class Invoice(models.Model):
    order = models.ForeignKey(SupplierOrder, on_delete=models.PROTECT, related_name='invoices')
    invoice_number = models.CharField(max_length=50)
    document_date = models.DateField()

    class Meta:
        verbose_name = 'Накладная'
        verbose_name_plural = 'Накладные'
        unique_together = [['order', 'invoice_number']]

    def __str__(self):
        return self.invoice_number
