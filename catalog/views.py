from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminRole
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['sku', 'name']
    search_fields = ['sku', 'name']

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsAdminRole()]
        return [IsAuthenticated()]
