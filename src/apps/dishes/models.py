from django.db import models

from core.models import TimestampedModel


class Dish(TimestampedModel):
    """Модель, представляющая блюдо в ресторане."""

    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name
