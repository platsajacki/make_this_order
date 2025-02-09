from typing import Any

from rest_framework import serializers

from apps.dishes.api.serializers import DishSerializer
from apps.dishes.models import Dish
from apps.orders.models import Order, OrderItem
from apps.tables.api.serializers import TableSerializer
from apps.tables.models import Table


class OrderItemWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания позиции заказа с выбором блюда по названию."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['dish'] = serializers.SlugRelatedField(
            queryset=Dish.objects.all(),
            slug_field='id',
        )

    class Meta:
        model = OrderItem
        fields = ['dish', 'quantity']


class OrderItemReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения позиции заказа."""

    dish = DishSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'dish', 'quantity', 'total_price']


class OrderReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения данных о заказе."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Инициализация сериализатора. В зависимости от флага is_reading выбирается
        соответствующий сериализатор для поля 'items'.
        """
        is_reading = kwargs.pop('is_reading', True)
        super().__init__(*args, **kwargs)
        if is_reading:
            self.fields['items'] = OrderItemReadSerializer(many=True, source='order_items')
        else:
            self.fields['items'] = OrderItemWriteSerializer(many=True)

    table = TableSerializer()

    class Meta:
        model = Order
        fields = [
            'id',
            'table',
            'items',
            'status',
            'total_price',
        ]


class OrderWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заказа."""

    items = OrderItemWriteSerializer(many=True)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['table'] = serializers.SlugRelatedField(
            queryset=Table.objects.all(),
            slug_field='number',
        )

    class Meta:
        model = Order
        fields = ['table', 'items', 'status']

    def to_representation(self, instance: Order) -> dict:
        """
        Сериализация объекта заказа в формат для ответа. Используется сериализатор
        для чтения (OrderReadSerializer) с флагом is_reading=False для использования
        сериализатора для записи.

        :param instance: Экземпляр объекта заказа, который нужно сериализовать.
        :return: Данные заказа в формате, соответствующем сериализатору для чтения.
        """
        return OrderReadSerializer(instance=instance, is_reading=False).data
