from django.contrib import admin

from .models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    """Админская модель для Table."""

    list_display = (
        'number',
        'seats',
        'description',
        'created',
        'updated',
    )
    list_filter = ('seats',)
    search_fields = (
        'number',
        'description',
    )
    ordering = ('number',)
    readonly_fields = (
        'created',
        'updated',
    )
