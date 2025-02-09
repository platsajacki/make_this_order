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
            slug_field='name',
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


class OrderWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заказа."""

    items = OrderItemReadSerializer(many=True)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['table_number'] = serializers.SlugRelatedField(
            queryset=Table.objects.all(),
            slug_field='number',
        )

    class Meta:
        model = Order
        fields = ['table_number', 'items', 'status']


class OrderReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения заказа."""

    items = OrderItemReadSerializer(many=True, source='order_items')
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
