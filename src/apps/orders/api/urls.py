from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.orders.api.views import OrderViewSet, ShiftRevenueAPIView

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('shift-revenue/', ShiftRevenueAPIView.as_view(), name='shift_revenue'),
]
