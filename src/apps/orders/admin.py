from decimal import Decimal

from django.contrib import admin

from apps.orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline модель для отображения позиций заказа в админке."""

    model = OrderItem
    extra = 1
    fields = ('dish', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Админская модель для заказа."""

    list_display = (
        'id',
        'table',
        'status',
        'total_price',
        'created',
        'updated',
    )
    list_filter = (
        'status',
        'created',
    )
    search_fields = (
        'id',
        'table__number',
    )
    readonly_fields = (
        'total_price',
        'created',
        'updated',
    )
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Админская модель для позиции заказа."""

    list_display = (
        'order',
        'dish',
        'quantity',
        'get_total_price',
    )
    search_fields = (
        'order__id',
        'dish__name',
    )
    fields = (
        'id',
        'order',
        'dish',
        'quantity',
        'get_total_price',
    )
    readonly_fields = (
        'id',
        'get_total_price',
        'created',
        'updated',
    )

    def get_total_price(self, obj: OrderItem) -> Decimal:
        """Возвращает общую стоимость блюда в заказе."""
        return obj.total_price

    get_total_price.short_description = 'Общая стоимость'  # type: ignore[attr-defined]
