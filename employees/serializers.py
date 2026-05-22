from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = Employee
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'position', 'department', 'email', 'groups',
        ]
        read_only_fields = fields
