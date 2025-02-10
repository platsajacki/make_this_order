import pytest

from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.parametrize(
    'method, url, data, excepted_status',
    [
        (
            'get',
            reverse('api_v1:dish-list'),
            None,
            status.HTTP_200_OK,
        ),
        (
            'get',
            reverse('api_v1:dish-detail', args=(2,)),
            None,
            status.HTTP_200_OK,
        ),
        (
            'get',
            reverse('api_v1:order-list'),
            None,
            status.HTTP_200_OK,
        ),
        (
            'get',
            reverse('api_v1:order-detail', args=(4,)),
            None,
            status.HTTP_200_OK,
        ),
        (
            'get',
            reverse('api_v1:shift-revenue'),
            None,
            status.HTTP_200_OK,
        ),
        (
            'get',
            reverse('api_v1:table-list'),
            None,
            status.HTTP_200_OK,
        ),
        (
            'get',
            reverse('api_v1:table-detail', args=(7,)),
            None,
            status.HTTP_200_OK,
        ),
        (
            'post',
            reverse('api_v1:order-list'),
            {'table': 1, 'items': [{'dish': 8, 'quantity': 3}]},
            status.HTTP_201_CREATED,
        ),
        (
            'patch',
            reverse('api_v1:order-detail', args=(10,)),
            {'status': 'ready'},
            status.HTTP_200_OK,
        ),
        (
            'delete',
            reverse('api_v1:order-detail', args=(11,)),
            None,
            status.HTTP_204_NO_CONTENT,
        ),
    ],
)
class TestAvailabilityAPIViewSet:
    def test_not_availability_viewset_without_auth(
        self, api_client: APIClient, method: str, url: str, data: dict | None, excepted_status: int
    ):
        response = getattr(api_client, method)(url, data=data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.usefixtures('dish', 'table', 'order')
    def test_availability_viewset_with_api_key_auth(
        self,
        api_client: APIClient,
        method: str,
        url: str,
        data: dict | None,
        excepted_status: int,
        auth_param: dict,
        order,
        table,
        dish,
    ):
        response = getattr(api_client, method)(url, data=data, headers=auth_param, format='json')
        assert response.status_code == excepted_status


class TestAvailabilityView:
    def test_not_availability_viewset_without_auth(self, client: Client):
        response = client.get(reverse('orders:list'))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_availability_viewset_with_auth(self, client: Client):
        client.force_login(get_user_model().objects.create(username='test', password='test'))
        response = client.get(reverse('orders:list'))
        assert response.status_code == status.HTTP_200_OK
