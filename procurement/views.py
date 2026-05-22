from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from core.permissions import GroupsPermission, user_in_group, user_in_any_group
from .models import PurchaseRequest, SupplierOrder, Invoice
from .serializers import (
    PurchaseRequestSerializer,
    PurchaseRequestStatusSerializer,
    SupplierOrderSerializer,
    InvoiceSerializer,
)


class PurchaseRequestViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseRequestSerializer
    filterset_fields = ['status', 'product']
    search_fields = ['id']
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_queryset(self):
        qs = PurchaseRequest.objects.select_related('product', 'created_by')
        user = self.request.user
        if user.is_superuser or user_in_group(user, 'purchaser') or user_in_group(user, 'manager'):
            return qs
        if user_in_group(user, 'storekeeper'):
            return qs.filter(created_by=user)
        return qs.none()

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        user = request.user
        if user.is_superuser:
            return
        if user_in_group(user, 'storekeeper') and obj.created_by_id != user.pk:
            raise PermissionDenied()
        if not user_in_any_group(user, 'purchaser', 'manager', 'storekeeper'):
            raise PermissionDenied()

    def list(self, request, *args, **kwargs):
        user = request.user
        if not user.is_superuser and not user_in_any_group(
            user, 'storekeeper', 'purchaser', 'manager'
        ):
            raise PermissionDenied()
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), GroupsPermission('storekeeper')()]
        if self.action in ('update', 'partial_update'):
            return [IsAuthenticated(), GroupsPermission('purchaser')()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return PurchaseRequestStatusSerializer
        return PurchaseRequestSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, status='new')

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(PurchaseRequestSerializer(instance).data)


class SupplierOrderViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierOrderSerializer
    filterset_fields = ['status', 'supplier']
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_queryset(self):
        return SupplierOrder.objects.select_related('request', 'supplier')

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), GroupsPermission('purchaser')()]
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated(), GroupsPermission('purchaser', 'manager', 'accountant')()]
        if self.action in ('update', 'partial_update'):
            return [IsAuthenticated(), GroupsPermission('purchaser')()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            if hasattr(exc, 'detail') and isinstance(exc.detail, dict) and 'alternatives' in exc.detail:
                return Response(
                    {
                        'error': True,
                        'message': exc.detail.get('detail', 'Поставщик не подходит'),
                        'alternatives': exc.detail.get('alternatives', []),
                    },
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
            raise
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        return Invoice.objects.select_related('order')

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), GroupsPermission('purchaser')()]
        return [IsAuthenticated(), GroupsPermission(
            'storekeeper', 'purchaser', 'manager', 'accountant'
        )()]
