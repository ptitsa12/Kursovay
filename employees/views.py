from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from core.permissions import user_in_group, IsManagerOrAdmin, IsAdminRole
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.all().order_by('id')

    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated(), IsManagerOrAdmin()]
        return [IsAuthenticated()]

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        user = request.user
        if user.is_superuser or user.is_staff or user_in_group(user, 'manager'):
            return
        if obj.pk != user.pk:
            raise PermissionDenied()
