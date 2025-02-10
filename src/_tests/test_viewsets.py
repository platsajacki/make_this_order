import pytest

from django.contrib.auth.models import AbstractBaseUser
from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.dishes.models import Dish
from apps.orders.models import Order


@pytest.mark.parametrize(
    'url',
    [
        reverse('api_v1:dish-list'),
        reverse('api_v1:order-list'),
        reverse('api_v1:table-list'),
        reverse('api_v1:shift-revenue'),
    ],
)
@pytest.mark.usefixtures('dish', 'table', 'order')
class TestAvailabilityAPIViewSetSafeWithoutArgs:
    def test_not_availability_viewset_without_auth(self, api_client: APIClient, url: str):
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_availability_viewset_with_api_key_auth(self, api_client: APIClient, auth_param: dict, url: str):
        response = api_client.get(url, headers=auth_param)
        assert response.status_code == status.HTTP_200_OK

    def test_availability_viewset_with_session_auth(
        self, api_client: APIClient, url: str, admin_user: AbstractBaseUser
    ):
        api_client.force_login(admin_user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    'url_name',
    [
        'api_v1:dish-detail',
        'api_v1:order-detail',
        'api_v1:table-detail',
    ],
)
@pytest.mark.usefixtures('dish', 'table', 'order')
class TestAvailabilityAPIViewSetSafeWithArgs:
    def test_not_availability_viewset_without_auth(self, api_client: APIClient, url_name: str):
        response = api_client.get(reverse(url_name, args=(1,)))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_availability_viewset_with_api_key_auth(
        self, api_client: APIClient, auth_param: dict, url_name: str, dish: Dish
    ):
        response = api_client.get(reverse(url_name, args=(dish.id,)), headers=auth_param)
        assert response.status_code == status.HTTP_200_OK

    def test_availability_viewset_with_session_auth(
        self, api_client: APIClient, url_name: str, admin_user: AbstractBaseUser, dish: Dish
    ):
        api_client.force_login(admin_user)
        response = api_client.get(reverse(url_name, args=(dish.id,)))
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.usefixtures('dish', 'table', 'order')
class TestPostOrderList:
    url = reverse('api_v1:order-list')

    def test_not_availability_viewset_without_auth(self, api_client: APIClient):
        assert Order.objects.count() == 1
        data = {'table': 1, 'items': [{'dish': 8, 'quantity': 3}]}
        response = api_client.post(self.url, data=data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Order.objects.count() == 1

    def test_availability_viewset_with_api_key_auth(self, api_client: APIClient, auth_param: dict, dish: Dish):
        assert Order.objects.count() == 1
        data = {'table': 1, 'items': [{'dish': dish.id, 'quantity': 3}]}
        response = api_client.post(self.url, data=data, headers=auth_param, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Order.objects.count() == 2

    def test_availability_viewset_with_session_auth(
        self, api_client: APIClient, admin_user: AbstractBaseUser, dish: Dish
    ):
        assert Order.objects.count() == 1
        data = {'table': 1, 'items': [{'dish': dish.id, 'quantity': 3}]}
        api_client.force_login(admin_user)
        response = api_client.post(self.url, data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Order.objects.count() == 2


@pytest.mark.usefixtures('dish', 'table', 'order')
class TestPatchOrderDetail:
    url_name = 'api_v1:order-detail'
    data = {'status': 'ready'}

    def test_not_availability_viewset_without_auth(self, api_client: APIClient):
        url = reverse(self.url_name, args=(10,))
        response = api_client.patch(url, data=self.data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_availability_viewset_with_api_key_auth(self, api_client: APIClient, auth_param: dict, order: Order):
        assert Order.objects.count() == 1
        url = reverse(self.url_name, args=(order.id,))
        response = api_client.patch(url, data=self.data, headers=auth_param, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert Order.objects.count() == 1
        assert Order.objects.get().status == self.data['status']

    @pytest.mark.usefixtures('dish', 'table', 'order')
    def test_availability_viewset_with_session_auth(
        self, api_client: APIClient, admin_user: AbstractBaseUser, order: Order
    ):
        assert Order.objects.count() == 1
        url = reverse(self.url_name, args=(order.id,))
        api_client.force_login(admin_user)
        response = api_client.patch(url, data=self.data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert Order.objects.count() == 1
        assert Order.objects.get().status == self.data['status']


class TestDeleteOrderDetail:
    url_name = 'api_v1:order-detail'

    def test_not_availability_viewset_without_auth(self, api_client: APIClient):
        url = reverse(self.url_name, args=(11,))
        response = api_client.delete(url, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.usefixtures('dish', 'table', 'order')
    def test_availability_viewset_with_api_key_auth(self, api_client: APIClient, auth_param: dict, order: Order):
        assert Order.objects.count() == 1
        url = reverse(self.url_name, args=(order.id,))
        response = api_client.delete(url, headers=auth_param, format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Order.objects.count() == 0

    @pytest.mark.usefixtures('dish', 'table', 'order')
    def test_availability_viewset_with_session_auth(
        self, api_client: APIClient, admin_user: AbstractBaseUser, order: Order
    ):
        assert Order.objects.count() == 1
        url = reverse(self.url_name, args=(order.id,))
        api_client.force_login(admin_user)
        response = api_client.delete(url, format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Order.objects.count() == 0


class TestAvailabilityView:
    def test_not_availability_viewset_without_auth(self, client: Client):
        response = client.get(reverse('orders:list'))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_availability_viewset_with_auth(self, admin_client: Client):
        response = admin_client.get(reverse('orders:list'))
        assert response.status_code == status.HTTP_200_OK
