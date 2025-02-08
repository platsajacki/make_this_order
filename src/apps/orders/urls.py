from django.urls import path

from apps.orders.views import OrderTemplateView

app_name = 'orders'

urlpatterns = [
    path('', OrderTemplateView.as_view(), name='list'),
]
