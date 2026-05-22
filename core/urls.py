from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from employees.views import EmployeeViewSet
from suppliers.views import SupplierViewSet
from catalog.views import ProductViewSet
from procurement.views import PurchaseRequestViewSet, SupplierOrderViewSet, InvoiceViewSet
from warehouse.views import (
    MaterialAcceptanceViewSet,
    QuantityCheckViewSet,
    SerialCheckViewSet,
    DeviationViewSet,
)
from finance.views import AccountableRequestViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'requests', PurchaseRequestViewSet, basename='request')
router.register(r'orders', SupplierOrderViewSet, basename='order')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'acceptances', MaterialAcceptanceViewSet, basename='acceptance')
router.register(r'quantity-checks', QuantityCheckViewSet, basename='quantity-check')
router.register(r'serial-checks', SerialCheckViewSet, basename='serial-check')
router.register(r'deviations', DeviationViewSet, basename='deviation')
router.register(r'accountable-requests', AccountableRequestViewSet, basename='accountable-request')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/', include(router.urls)),
]
