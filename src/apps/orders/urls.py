from django.urls import path

from apps.orders.views import TemplateView

app_name = 'orders'

urlpatterns = [
    path('', TemplateView.as_view(), name='list'),
]
