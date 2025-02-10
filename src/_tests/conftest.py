import pytest

from rest_framework.test import APIClient
from rest_framework_api_key.models import APIKey

from mimesis import Field, Fieldset, Generic, Schema
from mimesis.locales import Locale

from apps.dishes.models import Dish
from apps.orders.models import Order, OrderItem
from apps.tables.models import Table


class FixtureFactory:
    def __init__(self) -> None:
        self.generic = Generic(locale=Locale.RU)
        self.field = Field(locale=Locale.RU)
        self.fieldset = Fieldset(locale=Locale.RU)
        self.schema = Schema


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def factory() -> FixtureFactory:
    return FixtureFactory()


@pytest.fixture
def api_key(factory: FixtureFactory) -> str:
    _, key = APIKey.objects.create_key(name=factory.field('word'))
    return key


@pytest.fixture
def auth_param(api_key: str) -> dict:
    return {'Authorization': f'Api-Key {api_key}'}


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def dish_data(factory: FixtureFactory) -> list[dict]:
    return factory.schema(
        lambda: {
            'name': factory.field('word'),
            'price': factory.generic.finance.price(),
        },
        iterations=10,
    ).create()


@pytest.fixture
def dish(dish_data: list[dict]) -> Dish:
    return Dish.objects.create(**dish_data[0])


@pytest.fixture
def table_data(factory: FixtureFactory) -> list[dict]:
    return factory.schema(
        lambda: {
            'number': factory.generic.numeric.integers(start=2, end=300)[0],
            'seats': factory.generic.numeric.integers()[2],
            'description': factory.field('word'),
        },
        iterations=10,
    ).create()


@pytest.fixture
def table(table_data: list[dict]) -> Table:
    return Table.objects.create(**table_data[0])


@pytest.fixture
def order(table: Table, dish: Dish) -> Order:
    table.number = 1
    table.save()
    order = Order.objects.create(table=table)
    OrderItem.objects.create(order=order, dish=dish)
    return order
