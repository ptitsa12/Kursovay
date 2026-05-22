from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.permissions import GroupsPermission
from .models import AccountableRequest, Approval
from .serializers import AccountableRequestSerializer, ApproveAccountableSerializer


class AccountableRequestViewSet(viewsets.ModelViewSet):
    serializer_class = AccountableRequestSerializer
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        return AccountableRequest.objects.select_related('order', 'created_by')

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), GroupsPermission('purchaser')()]
        if self.action == 'approve':
            return [IsAuthenticated(), GroupsPermission('manager')()]
        return [IsAuthenticated(), GroupsPermission('purchaser', 'manager', 'accountant')()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, status='pending')

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        accountable = self.get_object()
        ser = ApproveAccountableSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        decision = ser.validated_data['decision']
        comment = ser.validated_data.get('comment', '')

        Approval.objects.create(
            request=accountable,
            approver=request.user,
            decision=decision,
            comment=comment,
        )
        accountable.status = 'approved' if decision == 'approved' else 'rejected'
        accountable.save(update_fields=['status'])

        return Response(AccountableRequestSerializer(accountable).data)
