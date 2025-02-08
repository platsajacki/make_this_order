from django.contrib import admin
from django.forms import Form
from django.http.request import HttpRequest

from apps.orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline модель для отображения позиций заказа в админке."""

    model = OrderItem
    extra = 1
    fields = ('dish', 'quantity', 'total_price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Админская модель для заказа."""

    list_display = (
        'id',
        'table_number',
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
        'table_number__number',
    )
    readonly_fields = (
        'total_price',
        'created',
        'updated',
    )
    inlines = [OrderItemInline]

    def save_model(self, request: HttpRequest, obj: Order, form: Form, change: bool) -> None:
        """Обновляем общюю стоимость перед сохранением."""
        obj.update_total_price()
        super().save_model(request, obj, form, change)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Админская модель для позиции заказа."""

    list_display = (
        'order',
        'dish',
        'quantity',
        'total_price',
    )
    search_fields = (
        'order__id',
        'dish__name',
    )
