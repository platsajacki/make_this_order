from rest_framework import serializers

from apps.dishes.models import Dish


class DishSerializer(serializers.ModelSerializer):
    """Сериализатор для блюд."""

    class Meta:
        model = Dish
        fields = ['id', 'name', 'price']
        read_only_fields = ['id']
