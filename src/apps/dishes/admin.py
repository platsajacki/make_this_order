from django.contrib import admin

from .models import Dish


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    list_filter = ('price',)
    search_fields = ('name',)
    fields = (
        'name',
        'price',
        'created',
        'updated',
    )
    ordering = ('name',)
    readonly_fields = (
        'created',
        'updated',
    )
