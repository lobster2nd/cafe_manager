import pytest
from django.urls import reverse

from rest_framework.test import APIClient

from manager_app.models import MenuItem, Order


@pytest.fixture
def client():
    """Фикстура для клиента API"""
    return APIClient()


@pytest.fixture
def menu_item():
    """Фикстура для создания пункта меню"""
    return MenuItem.objects.create(name="Pizza", price=10.00)


@pytest.fixture
def order(menu_item):
    """Фикстура для создания заказа"""
    order = Order.objects.create(table_number=1)
    order.items.add(menu_item)
    return order


@pytest.fixture
def order_list_url():
    """Фикстура для получения URL списка заказов"""
    return reverse('orders-list')


@pytest.fixture
def order_detail_url(order):
    """Фикстура для получения URL конкретного заказа"""
    return reverse('orders-detail', args=[order.id])


@pytest.fixture
def menu_item_list_url():
    """Фикстура для получения URL списка пунктов меню"""
    return reverse('menu_items-list')


@pytest.fixture
def menu_item_detail_url(menu_item):
    """Фикстура для получения URL конкретного пункта меню"""
    return reverse('menu_items-detail', args=[menu_item.id])

