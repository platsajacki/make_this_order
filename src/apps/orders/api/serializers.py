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
    """Сериализатор для чтения данных о заказе.

    Этот сериализатор используется для извлечения данных о заказах. В зависимости от переданных параметров,
    он может изменять способ представления связанных объектов заказа.

    Параметры kwargs:
        - source (bool): Флаг, указывающий, использовать ли source для поля 'items'.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Инициализация сериализатора. В зависимости от флага 'source' выбирается
        соответствующий сериализатор для поля 'items'.

        :param args: Позиционные аргументы для инициализации родительского класса.
        :param kwargs: Ключевые аргументы, включая флаг 'source', определяющий использование данных для поля 'items'.
        """
        source = kwargs.pop('source', True)
        super().__init__(*args, **kwargs)
        if source:
            self.fields['items'] = OrderItemReadSerializer(many=True, source='order_items')
        else:
            self.fields['items'] = OrderItemReadSerializer(many=True)

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
        """Инициализация сериализатора.

        В конструкторе устанавливается поле 'table', которое является выбором столика по его номеру.
        """
        super().__init__(*args, **kwargs)
        self.fields['table'] = serializers.SlugRelatedField(
            queryset=Table.objects.all(),
            slug_field='number',
        )

    class Meta:
        model = Order
        fields = ['table', 'items', 'status']


class OrderPostSerializer(OrderWriteSerializer):
    """Сериализатор для создания нового заказа через POST запрос.

    Этот сериализатор расширяет `OrderWriteSerializer` и используется
    для обработки POST-запросов на создание заказа. Он преобразует объект
    заказа в формат данных для ответа с использованием `OrderReadSerializer`
    с флагом source=False.
    """

    def to_representation(self, instance: Order) -> dict:
        """Преобразует экземпляр заказа в формат данных для ответа."""
        return OrderReadSerializer(instance=instance, source=False).data

    def validate_items(self, value: list) -> list:
        if not value:
            raise serializers.ValidationError('Поле `items` не может быть пустым.')
        return value


class OrderPatchSerializer(OrderWriteSerializer):
    """Сериализатор для частичного обновления заказа через PATCH запрос.

    Этот сериализатор расширяет `OrderWriteSerializer` и используется
    для обработки PATCH-запросов на частичное обновление заказа. Он
    преобразует объект заказа в формат данных для ответа с использованием
    `OrderReadSerializer` без изменения флага.
    """

    def to_representation(self, instance: Order) -> dict:
        """Преобразует экземпляр заказа в формат данных для ответа."""
        return OrderReadSerializer(instance=instance).data


class ShiftRevenueSerializer(serializers.Serializer):
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
