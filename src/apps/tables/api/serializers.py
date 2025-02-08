from rest_framework import serializers

from apps.tables.models import Table


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'number', 'seats', 'description']
        read_only_fields = ['id']
