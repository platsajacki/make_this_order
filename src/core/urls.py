from django.contrib import admin
from django.urls import include, path

from django.contrib.auth.views import LoginView
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
        title='Make This Order',
        default_version='v1',
        description="Api Docs",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


api_v1 = [
    path('', include('apps.dishes.api.urls')),
    path('', include('apps.orders.api.urls')),
    path('', include('apps.tables.api.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('api/v1/', include(api_v1), name='api_v1'),
    path('orders/', include('apps.orders.urls')),
]
