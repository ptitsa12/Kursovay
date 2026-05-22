from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    list_display = ('username', 'last_name', 'first_name', 'position', 'department', 'is_staff')
    list_filter = ('department', 'is_staff', 'groups')
    search_fields = ('username', 'last_name', 'first_name', 'email')
    filter_horizontal = ('groups', 'user_permissions')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('position', 'department')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительно', {'fields': ('position', 'department')}),
    )
