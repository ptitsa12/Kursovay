from rest_framework import serializers
from .models import AccountableRequest, Approval


class AccountableRequestSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AccountableRequest
        fields = [
            'id', 'order', 'amount', 'due_date', 'status', 'created_by',
        ]
        read_only_fields = ['status', 'created_by']


class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approval
        fields = ['id', 'request', 'approver', 'decision', 'comment', 'decided_at']
        read_only_fields = ['approver', 'decided_at']


class ApproveAccountableSerializer(serializers.Serializer):
    decision = serializers.ChoiceField(choices=['approved', 'rejected'])
    comment = serializers.CharField(required=False, allow_blank=True)
