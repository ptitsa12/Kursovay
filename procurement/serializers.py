from decimal import Decimal
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from suppliers.models import Supplier
from suppliers.serializers import SupplierSerializer
from .models import PurchaseRequest, SupplierOrder, Invoice


class PurchaseRequestSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    created_by_id = serializers.IntegerField(read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = PurchaseRequest
        fields = [
            'id', 'product', 'product_name', 'quantity', 'desired_date',
            'status', 'created_by', 'created_by_id', 'created_at',
        ]
        read_only_fields = ['status', 'created_by', 'created_by_id', 'created_at']

    def validate(self, attrs):
        if self.instance is None:
            return attrs
        if 'status' in attrs and len(attrs) == 1:
            return attrs
        return attrs


class PurchaseRequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseRequest
        fields = ['status']

    def validate_status(self, value):
        if value not in ('accepted', 'rejected'):
            raise serializers.ValidationError('Допустимы статусы: accepted, rejected')
        return value


class SupplierOrderSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(read_only=True)
    request_id = serializers.IntegerField(source='request.id', read_only=True)

    class Meta:
        model = SupplierOrder
        fields = [
            'id', 'request', 'request_id', 'supplier', 'amount',
            'order_date', 'status', 'order_number',
        ]
        read_only_fields = ['order_date', 'order_number']

    def validate(self, attrs):
        supplier = attrs.get('supplier')
        if supplier is None and self.instance:
            supplier = self.instance.supplier
        if supplier is None:
            return attrs

        if not supplier.is_active or supplier.rating < Decimal('3.0'):
            alternatives = Supplier.objects.filter(
                is_active=True, rating__gte=Decimal('3.0')
            ).exclude(pk=supplier.pk)
            raise ValidationError({
                'detail': 'Поставщик неактивен или рейтинг ниже 3.0. Выберите альтернативу.',
                'alternatives': SupplierSerializer(alternatives, many=True).data,
            })
        return attrs

    def create(self, validated_data):
        request_obj = validated_data['request']
        if request_obj.status != 'accepted':
            raise ValidationError({'detail': 'Заявка должна быть в статусе accepted'})
        if hasattr(request_obj, 'supplierorder'):
            raise ValidationError({'detail': 'Заказ по этой заявке уже существует'})
        return super().create(validated_data)


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'order', 'invoice_number', 'document_date']
