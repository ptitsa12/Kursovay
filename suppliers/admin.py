from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'inn', 'is_active', 'rating', 'email')
    list_filter = ('is_active',)
    search_fields = ('name', 'inn', 'email')
    readonly_fields = ()
