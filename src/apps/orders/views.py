from django.views.generic import ListView

from apps.orders.models import Order


class OrderListView(ListView):
    model = Order
