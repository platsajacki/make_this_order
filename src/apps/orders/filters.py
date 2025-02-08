from django_filters import CharFilter, FilterSet, NumberFilter

from apps.orders.models import Order


class OrderFilterSet(FilterSet):
    """
    Фильтр для модели 'Order' (заказ), который позволяет фильтровать заказы по статусу и номеру стола.

    Этот фильтр позволяет API фильтровать заказы по следующим полям:
    - 'status' — статус заказа (например, "pending", "ready", "completed"). Сравнение без учета регистра.
    - 'table_number' — номер стола, к которому привязан заказ. Для этого используется поле 'number' модели 'Table'.

    Пример использования:
    - /api/orders/?status=ready&table_number=1
    - Этот запрос вернет все заказы со статусом 'ready' и номером стола 1.
    """

    status = CharFilter(
        field_name='status',
        lookup_expr='iexact',
    )
    table_number = NumberFilter(
        field_name='table_number__number',
    )

    class Meta:
        model = Order
        fields = ['status', 'table_number']
