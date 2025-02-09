from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.tables.api.views import TableViewSet

router = DefaultRouter()
router.register(r'tables', TableViewSet, basename='table')

urlpatterns = [
    path('', include(router.urls)),
]
