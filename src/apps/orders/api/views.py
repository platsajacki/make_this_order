from typing import Any

from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_api_key.permissions import HasAPIKey

from apps.orders.api.serializers import (
    OrderPatchSerializer,
    OrderPostSerializer,
    OrderReadSerializer,
    OrderWriteSerializer,
)
from apps.orders.filters import OrderFilterSet
from apps.orders.models import Order
from apps.orders.services.order_creator import OrderCreator
from apps.orders.services.order_updater import OrderUpdater
from apps.orders.services.total_revenue_getter import ShiftRevenueGetter

OrderSerializers = OrderReadSerializer | OrderWriteSerializer | OrderPostSerializer | OrderPatchSerializer


class OrderViewSet(ModelViewSet):
    """
    ViewSet для управления заказами.

    Данный ViewSet предоставляет доступ к заказам и поддерживает стандартные
    операции CRUD (создание, получение, обновление, удаление).

    Особенности:
    - Использует сериализатор OrderReadSerializer для представления данных.
    - Фильтрует заказы с помощью OrderFilterSet.
    - Требует аутентификацию пользователя (IsAuthenticated) или API-ключ (HasAPIKey).
    - Оптимизирует запросы с помощью select_related и prefetch_related:
      - select_related('table') загружает связанные данные о номере стола.
      - prefetch_related('order_items__dish') загружает связанные блюда в заказе.
    """

    model = Order
    serializer_class = OrderReadSerializer
    permission_classes = [IsAuthenticated | HasAPIKey]
    queryset = Order.objects.select_related('table').prefetch_related('order_items__dish')
    filterset_class = OrderFilterSet
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self) -> OrderSerializers:
        method = self.request.method
        if method in SAFE_METHODS:
            return OrderReadSerializer
        if method == 'PATCH':
            return OrderPatchSerializer
        if method == 'POST':
            return OrderPostSerializer
        return OrderWriteSerializer

    def perform_create(self, serializer: OrderWriteSerializer) -> Order:
        return OrderCreator(serializer)()

    def perform_update(self, serializer: OrderWriteSerializer) -> Order:
        return OrderUpdater(serializer)()


class ShiftRevenueAPIView(APIView):
    """Представление для получения общей выручки."""

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return ShiftRevenueGetter()()
