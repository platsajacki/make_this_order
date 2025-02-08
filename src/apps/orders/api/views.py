from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_api_key.permissions import HasAPIKey

from apps.orders.api.serializers import OrderReadSerializer
from apps.orders.filters import OrderFilterSet
from apps.orders.models import Order


class OrderViewSet(ModelViewSet):
    model = Order
    serializer_class = OrderReadSerializer
    permission_classes = [IsAuthenticated | HasAPIKey]
    queryset = Order.objects.all()
    filterset_class = OrderFilterSet
