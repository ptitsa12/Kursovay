from django.contrib import admin
from .models import PurchaseRequest, SupplierOrder, Invoice


@admin.register(PurchaseRequest)
class PurchaseRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'desired_date')
    search_fields = ('id', 'product__name', 'created_by__username')
    readonly_fields = ('created_at',)


@admin.register(SupplierOrder)
class SupplierOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'request', 'supplier', 'amount', 'status', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('order_number', 'supplier__name')
    readonly_fields = ('order_number', 'order_date')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'order', 'document_date')
    list_filter = ('document_date',)
    search_fields = ('invoice_number',)
