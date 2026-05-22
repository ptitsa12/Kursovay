from django.db import models
from employees.models import Employee
from procurement.models import SupplierOrder


class AccountableRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На утверждении'),
        ('approved', 'Утверждена'),
        ('rejected', 'Отклонена'),
    ]
    order = models.ForeignKey(SupplierOrder, on_delete=models.PROTECT, related_name='accountable_requests')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='accountable_requests')

    class Meta:
        verbose_name = 'Заявка на подотчёт'
        verbose_name_plural = 'Заявки на подотчёт'

    def __str__(self):
        return f'Подотчёт #{self.id}'


class Approval(models.Model):
    DECISION_CHOICES = [
        ('approved', 'Утверждено'),
        ('rejected', 'Отклонено'),
    ]
    request = models.ForeignKey(AccountableRequest, on_delete=models.CASCADE, related_name='approvals')
    approver = models.ForeignKey(Employee, on_delete=models.PROTECT)
    decision = models.CharField(max_length=10, choices=DECISION_CHOICES)
    comment = models.TextField(blank=True)
    decided_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Согласование'
        verbose_name_plural = 'Согласования'
