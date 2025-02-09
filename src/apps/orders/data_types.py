from typing import TypedDict

from apps.dishes.models import Dish
from apps.tables.models import Table


class OrderItemData(TypedDict):
    dish: Dish
    quantity: int


class OrderValidatedData(TypedDict):
    table: Table
    items: list[OrderItemData]
