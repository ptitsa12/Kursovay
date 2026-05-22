from rest_framework import serializers
from .models import MaterialAcceptance, QuantityCheck, SerialCheck, Deviation


class MaterialAcceptanceSerializer(serializers.ModelSerializer):
    accepted_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MaterialAcceptance
        fields = ['id', 'invoice', 'acceptance_date', 'accepted_by']
        read_only_fields = ['acceptance_date', 'accepted_by']


class QuantityCheckSerializer(serializers.ModelSerializer):
    result = serializers.CharField(read_only=True)

    class Meta:
        model = QuantityCheck
        fields = [
            'id', 'acceptance', 'product', 'declared_quantity',
            'actual_quantity', 'result',
        ]
        read_only_fields = ['result']


class SerialCheckSerializer(serializers.ModelSerializer):
    is_unique = serializers.BooleanField(read_only=True)

    class Meta:
        model = SerialCheck
        fields = ['id', 'acceptance', 'product', 'serial_number', 'is_unique']
        read_only_fields = ['is_unique']


class DeviationSerializer(serializers.ModelSerializer):
    detected_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Deviation
        fields = ['id', 'acceptance', 'deviation_type', 'description', 'detected_by']
        read_only_fields = ['detected_by']
