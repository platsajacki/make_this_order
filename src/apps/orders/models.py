from typing import Any

from django.db import models

from apps.dishes.models import Dish
from apps.tables.models import Table
from core.models import TimestampedModel


class OrderStatus(models.TextChoices):
    PENDING = 'pending', 'В ожидании'
    READY = 'ready', 'Готово'
    PAID = 'paid', 'Оплачено'


class Order(TimestampedModel):
    """Модель, представляющая заказ в ресторане."""

    table_number = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        verbose_name='Стол',
    )
    items = models.ManyToManyField(  # type: ignore[var-annotated]
        Dish,
        through='OrderItem',
        verbose_name='Заказанные блюда',
    )
    total_price = models.DecimalField(
        verbose_name='Общая стоимость',
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    status = models.CharField(
        verbose_name='Статус заказа',
        max_length=10,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']

    def __str__(self) -> str:
        return f'Заказ №{self.id} для стола {self.table_number.number}'

    def update_total_price(self) -> None:
        """Метод для вычисления общей стоимости заказа."""
        self.total_price = sum([item.total_price for item in self.order_items.all()])
        self.save()


class OrderItem(TimestampedModel):
    """Модель для связи блюда и заказа с количеством и ценой."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='order_items',
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        verbose_name='Блюдо',
        related_name='order_items',
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        default=1,
    )

    @property
    def total_price(self):
        """Метод для вычисления общей стоимости блюда в заказе."""
        return self.dish.price * self.quantity

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'
        ordering = ['order']

    def __str__(self) -> str:
        return f'{self.dish.name} (x{self.quantity})'
