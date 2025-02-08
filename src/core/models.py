from django.db import models


class TimestampedModel(models.Model):
    """Абстарктная модель с полями 'created' и 'updated'."""

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения',
    )

    class Meta:
        abstract = True
