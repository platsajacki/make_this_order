from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_api_key.permissions import HasAPIKey

from apps.tables.api.serializers import TableSerializer
from apps.tables.models import Table


class TableViewSet(ReadOnlyModelViewSet):
    """ViewSet для чтения столов."""

    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated | HasAPIKey]
