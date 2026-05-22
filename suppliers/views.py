from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.permissions import GroupsPermission
from .models import Supplier
from .serializers import SupplierSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filterset_fields = ['is_active', 'name']
    search_fields = ['name', 'inn']

    def get_permissions(self):
        if self.action in ('list',):
            return [IsAuthenticated(), GroupsPermission('purchaser', 'manager', 'accountant')()]
        if self.action in ('retrieve', 'update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), GroupsPermission('purchaser', 'manager')()]
        if self.action == 'create':
            return [IsAuthenticated(), GroupsPermission('purchaser')()]
        return [IsAuthenticated()]
