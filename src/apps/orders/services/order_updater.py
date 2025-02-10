from dataclasses import dataclass

from django.db.transaction import atomic

from apps.orders.api.serializers import OrderPatchSerializer
from apps.orders.data_types import OrderValidatedData
from apps.orders.models import Order, OrderItem
from core.services import BaseService


@dataclass
class OrderUpdater(BaseService):
    """
    Сервис для обновления существующего заказа с его позициями.

    Этот сервис используется для обновления заказа на основе валидированных данных.
    Он принимает сериализатор, который обрабатывает данные для обновления заказа, и
    выполняет обновление самого заказа и его позиций в базе данных.

    Атрибуты:
        serializer (OrderPatchSerializer): Сериализатор для обновления заказа.
    """

    serializer: OrderPatchSerializer

    def update(self, data: OrderValidatedData, order: Order) -> Order:
        """
        Обновляет заказ и его позиции в базе данных.

        :param data: Валидированные данные о заказе, содержащие информацию о заказе и его позициях.
        :return: Обновленный объект заказа.
        """
        with atomic():
            if items_data := data.pop('items', None):
                order.order_items.all().delete()
                order_items = [OrderItem(order=order, **item_data) for item_data in items_data]
                OrderItem.objects.bulk_create(order_items)
                order.update_total_price()
            for field, value in data.items():
                if hasattr(order, field):
                    setattr(order, field, value)
            order.save()
        return order

    def act(self) -> Order:
        """
        Выполняет обновление заказа, используя сериализатор для получения валидированных данных.

        :return: Обновленный объект заказа.
        """
        data = self.serializer.validated_data
        return self.update(data, self.serializer.instance)
