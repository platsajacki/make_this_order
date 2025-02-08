from django.db import models

from core.models import TimestampedModel


class Table(TimestampedModel):
    """Модель, представляющая стол в ресторане."""

    number = models.PositiveBigIntegerField(
        verbose_name='Номер стола',
        unique=True,
    )
    seats = models.PositiveIntegerField(
        verbose_name='Количество мест',
    )
    description = models.CharField(
        verbose_name='Описание',
        max_length=256,
    )

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'
        ordering = ['number']

    def __str__(self) -> str:
        return f'Стол №{self.number}'
