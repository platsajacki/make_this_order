import pytest

from rest_framework.test import APIClient
from rest_framework_api_key.models import APIKey

from mimesis import Field, Fieldset, Generic, Schema
from mimesis.builtins import RussiaSpecProvider
from mimesis.locales import Locale


class FixtureFactory:
    def __init__(self) -> None:
        self.generic = Generic(locale=Locale.RU)
        self.field = Field(locale=Locale.RU)
        self.fieldset = Fieldset(locale=Locale.RU)
        self.schema = Schema
        self.russia = RussiaSpecProvider()


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

