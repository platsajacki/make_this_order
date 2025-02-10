from dataclasses import dataclass

from django.db.transaction import atomic

from apps.orders.api.serializers import OrderPostSerializer
from apps.orders.data_types import OrderValidatedData
from apps.orders.models import Order, OrderItem
from core.services import BaseService


@dataclass
class OrderCreator(BaseService):
    """
    Сервис для создания заказа с позициями.

    Этот сервис используется для создания нового заказа на основе валидированных данных.
    Он принимает сериализатор, который обрабатывает данные для создания заказа, и
    выполняет создание самого заказа и его позиций в базе данных.

    Атрибуты:
        serializer (OrderPostSerializer): Сериализатор для создания заказа.
    """

    serializer: OrderPostSerializer

    def create(self, data: OrderValidatedData) -> Order:
        """
        Создает заказ в базе данных и сохраняет его позиции.

        :param data: Валидированные данные о заказе, содержащие информацию о заказе и позициях.
        :return: Созданный объект заказа.
        """
        with atomic():
            order = Order.objects.create(table=data['table'])
            order_items = [OrderItem(order=order, **item_data) for item_data in data['items']]
            OrderItem.objects.bulk_create(order_items)
            order.update_total_price()
        return order

    def act(self) -> Order:
        """
        Выполняет создание заказа, используя сериализатор для получения валидированных данных.

        :return: Созданный объект заказа.
        """
        data = self.serializer.validated_data
        return self.create(data)
