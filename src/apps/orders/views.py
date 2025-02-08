from django.views.generic import TemplateView


class OrderTemplateView(TemplateView):
    template_name = 'orders/order_list.html'
