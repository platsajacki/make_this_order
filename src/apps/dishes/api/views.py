from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_api_key.permissions import HasAPIKey

from apps.dishes.api.serializers import DishSerializer
from apps.dishes.models import Dish


class DishViewSet(ReadOnlyModelViewSet):
    """ViewSet для чтения блюд."""

    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated | HasAPIKey]
