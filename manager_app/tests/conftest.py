import pytest
from django.urls import reverse
from django.test import Client

from manager_app.models import MenuItem, Order


@pytest.fixture
def menu_item():
    """Фикстура для создания пункта меню"""
    return MenuItem.objects.create(name="Пицца", price=10.99)


@pytest.fixture
def another_menu_item():
    """Фикстура для создания другого пункта меню"""
    return MenuItem.objects.create(name="Паста", price=8.50)


@pytest.fixture
def order(menu_item, another_menu_item):
    """Фикстура для создания заказа с пунктами меню"""
    order = Order.objects.create(table_number=1)
    order.items.add(menu_item, another_menu_item)
    return order


@pytest.fixture
def client():
    """Фикстура для клиента"""
    return Client()


@pytest.fixture
def create_orders(db):
    """Фикстура для создания тестовых заказов"""
    Order.objects.create(table_number=1, status='pending')
    Order.objects.create(table_number=2, status='completed')
    Order.objects.create(table_number=1, status='pending')


@pytest.fixture
def order_list_url():
    """Фикстура для получения URL списка заказов"""
    return reverse('home')


@pytest.fixture
def order_f(create_orders):
    """Фикстура для получения существующего заказа"""
    return Order.objects.first()


@pytest.fixture
def order_url():
    """Фикстура для получения URL создания заказа"""
    return reverse('add_order')


@pytest.fixture
def menu_item_url():
    """Фикстура для получения URL создания пункта меню"""
    return reverse('add_item')


@pytest.fixture
def order_detail_url(order_f):
    """Фикстура для получения URL деталей заказа"""
    return reverse('order_detail', args=[order_f.id])


@pytest.fixture
def order_update_url(order_f):
    """Фикстура для получения URL обновления статуса заказа"""
    return reverse('order_edit', args=[order_f.id])


@pytest.fixture
def order_delete_url(order_f):
    """Фикстура для получения URL удаления заказа"""
    return reverse('order_delete', args=[order_f.id])


@pytest.fixture
def revenue_url():
    """Фикстура для получения URL страницы выручки"""
    return reverse('total_revenue')

