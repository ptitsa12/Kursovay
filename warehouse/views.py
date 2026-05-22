from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from core.permissions import GroupsPermission, user_in_group
from .models import MaterialAcceptance, QuantityCheck, SerialCheck, Deviation
from .serializers import (
    MaterialAcceptanceSerializer,
    QuantityCheckSerializer,
    SerialCheckSerializer,
    DeviationSerializer,
)


class MaterialAcceptanceViewSet(viewsets.ModelViewSet):
    serializer_class = MaterialAcceptanceSerializer
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_queryset(self):
        return MaterialAcceptance.objects.select_related('invoice', 'accepted_by')

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), GroupsPermission('storekeeper')()]
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated(), GroupsPermission(
                'storekeeper', 'purchaser', 'accountant'
            )()]
        if self.action in ('update', 'partial_update'):
            return [IsAuthenticated(), GroupsPermission('storekeeper')()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(accepted_by=self.request.user)


class QuantityCheckViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = QuantityCheck.objects.all()
    serializer_class = QuantityCheckSerializer

    def get_permissions(self):
        return [IsAuthenticated(), GroupsPermission('storekeeper')()]


class SerialCheckViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = SerialCheck.objects.all()
    serializer_class = SerialCheckSerializer

    def get_permissions(self):
        return [IsAuthenticated(), GroupsPermission('storekeeper')()]


class DeviationViewSet(viewsets.ModelViewSet):
    serializer_class = DeviationSerializer
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        return Deviation.objects.select_related('acceptance', 'detected_by')

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), GroupsPermission('storekeeper')()]
        return [IsAuthenticated(), GroupsPermission(
            'purchaser', 'manager', 'accountant', 'storekeeper'
        )()]

    def perform_create(self, serializer):
        serializer.save(detected_by=self.request.user)
