from django.contrib import admin
from .models import AccountableRequest, Approval


@admin.register(AccountableRequest)
class AccountableRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'status', 'due_date', 'created_by')
    list_filter = ('status', 'due_date')
    search_fields = ('id',)


@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = ('request', 'approver', 'decision', 'decided_at')
    list_filter = ('decision',)
    readonly_fields = ('decided_at',)
