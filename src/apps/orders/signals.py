from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.orders.models import OrderItem


@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total_price(sender: OrderItem, instance: OrderItem, **kwargs):
    """Обновляем цену ордера."""
    instance.order.update_total_price()
