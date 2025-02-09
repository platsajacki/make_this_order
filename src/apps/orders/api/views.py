from typing import Any

from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_api_key.permissions import HasAPIKey

from apps.orders.api.serializers import OrderReadSerializer, OrderWriteSerializer
from apps.orders.filters import OrderFilterSet
from apps.orders.models import Order
from apps.orders.services.order_creator import OrderCreator


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

    def get_serializer(self, *args: Any, **kwargs: Any) -> OrderReadSerializer | OrderWriteSerializer:
        if self.request.method in SAFE_METHODS:
            return OrderReadSerializer(*args, **kwargs)
        return OrderWriteSerializer(*args, **kwargs)

    def perform_create(self, serializer: OrderWriteSerializer) -> Order:
        return OrderCreator(serializer)()

    def perform_update(self, serializer: OrderWriteSerializer) -> Order:
        return super().perform_update(serializer)
