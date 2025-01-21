from decimal import Decimal

import pytest

from manager_app.models import Order


@pytest.mark.django_db
class TestMenuItem:
    def test_create_menu_item(self, menu_item):
        """Тест на создание пункта меню"""
        assert menu_item.name == "Пицца"
        assert menu_item.price == 10.99

    def test_str_method(self, menu_item):
        """Тест на метод __str__"""
        assert str(menu_item) == "Пицца, цена - 10.99"


@pytest.mark.django_db
class TestOrder:
    def test_create_order(self, order):
        """Тест на создание заказа"""
        assert order.table_number == 1
        assert order.status == 'pending'
        assert order.items.count() == 2

    def test_total_price(self, order):
        """Тест на вычисление общей суммы заказа"""
        assert order.total_price == Decimal('19.49')

    def test_order_status_choices(self, order):
        """Тест на проверку статусов заказа"""
        assert order.status in dict(Order.STATUS_CHOICES).keys()