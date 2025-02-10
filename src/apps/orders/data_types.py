from datetime import datetime
from typing import NamedTuple, TypedDict

from apps.dishes.models import Dish
from apps.tables.models import Table


class OrderItemData(TypedDict):
    dish: Dish
    quantity: int


class OrderValidatedData(TypedDict, total=False):
    table: Table
    items: list[OrderItemData]


class WorkingTime(NamedTuple):
    start: datetime
    end: datetime
