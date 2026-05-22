from django.contrib import admin
from .models import MaterialAcceptance, QuantityCheck, SerialCheck, Deviation


@admin.register(MaterialAcceptance)
class MaterialAcceptanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'acceptance_date', 'accepted_by')
    list_filter = ('acceptance_date',)
    readonly_fields = ('acceptance_date',)


@admin.register(QuantityCheck)
class QuantityCheckAdmin(admin.ModelAdmin):
    list_display = ('acceptance', 'product', 'declared_quantity', 'actual_quantity', 'result')
    list_filter = ('result',)
    readonly_fields = ('result',)


@admin.register(SerialCheck)
class SerialCheckAdmin(admin.ModelAdmin):
    list_display = ('acceptance', 'product', 'serial_number', 'is_unique')
    readonly_fields = ('is_unique',)


@admin.register(Deviation)
class DeviationAdmin(admin.ModelAdmin):
    list_display = ('acceptance', 'deviation_type', 'detected_by')
    list_filter = ('deviation_type',)
    search_fields = ('description',)
