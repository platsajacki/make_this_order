from typing import Any

from django.http.request import HttpRequest
from django.http.response import HttpResponseBase, HttpResponseForbidden
from django.views.generic import TemplateView


class OrderTemplateView(TemplateView):
    template_name = 'orders/order_list.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        if request.user and request.user.is_anonymous:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
