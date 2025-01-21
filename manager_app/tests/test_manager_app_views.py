import pytest
from decimal import Decimal

from django.urls import reverse

from manager_app.models import Order, MenuItem


@pytest.mark.django_db
class TestOrderListView:
    def test_order_list_view(self, client, create_orders, order_list_url):
        """Тест на получение списка всех заказов"""
        response = client.get(order_list_url)
        assert response.status_code == 200
        assert len(response.context['orders']) == 3

    def test_order_list_view_filter_by_table_number(self, client,
                                                    create_orders,
                                                    order_list_url):
        """Тест на фильтрацию заказов по номеру стола"""
        response = client.get(order_list_url, {'table_number': 1})
        assert response.status_code == 200
        assert len(response.context['orders']) == 2

    def test_order_list_view_filter_by_status(self, client,
                                              create_orders,
                                              order_list_url):
        """Тест на фильтрацию заказов по статусу"""
        response = client.get(order_list_url, {'status': 'pending'})
        assert response.status_code == 200
        assert len(response.context['orders']) == 2


@pytest.mark.django_db
class TestAddOrderView:
    def test_add_order_view_get(self, client, order_url):
        """Тест на получение страницы создания заказа"""
        response = client.get(order_url)
        assert response.status_code == 200
        assert 'form' in response.context

    def test_add_order_view_post_valid_data(self, client, order_url, menu_item,
                                            another_menu_item):
        """Тест на создание заказа с валидными данными"""
        data = {
            'table_number': 1,
            'status': 'pending',
            'items': [menu_item.id, another_menu_item.id],
        }
        response = client.post(order_url, data)
        assert response.status_code == 302
        assert Order.objects.count() == 1
        order = Order.objects.first()
        assert order.table_number == 1
        assert list(order.items.values_list('id', flat=True)) == \
               [menu_item.id, another_menu_item.id]

    def test_add_order_view_post_invalid_data(self, client, order_url):
        """Тест на создание заказа с невалидными данными"""
        data = {
            'table_number': '',
            'status': 'pending',
        }
        response = client.post(order_url, data)
        assert response.status_code == 200
        assert 'form' in response.context
        assert Order.objects.count() == 0


@pytest.mark.django_db
class TestAddMenuItemView:
    def test_add_menu_item_view_get(self, client, menu_item_url):
        """Тест на получение страницы создания пункта меню"""
        response = client.get(menu_item_url)
        assert response.status_code == 200
        assert 'form' in response.context

    def test_add_menu_item_view_post_valid_data(self, client, menu_item_url):
        """Тест на создание пункта меню с валидными данными"""
        data = {
            'name': 'Салат',
            'price': 5.99,
        }
        response = client.post(menu_item_url, data)
        assert response.status_code == 302
        assert MenuItem.objects.count() == 1
        assert MenuItem.objects.first().name == 'Салат'
        assert MenuItem.objects.first().price == Decimal('5.99')

    def test_add_menu_item_view_post_invalid_data(self, client, menu_item_url):
        """Тест на создание пункта меню с невалидными данными"""
        data = {
            'name': '',
            'price': -1,
        }
        response = client.post(menu_item_url, data)
        assert response.status_code == 200
        assert 'form' in response.context
        assert MenuItem.objects.count() == 0


@pytest.mark.django_db
class TestOrderDetailView:
    def test_order_update_status_view_get(self, client, order_update_url):
        """Тест на получение страницы обновления статуса заказа"""
        response = client.get(order_update_url)
        assert response.status_code == 200
        assert 'form' in response.context

    def test_order_update_status_view_post_valid_data(self, client,
                                                      order_update_url,
                                                      order_f):
        """Тест на обновление статуса заказа с валидными данными"""
        data = {
            'status': 'paid',
        }
        response = client.post(order_update_url, data)
        assert response.status_code == 302
        order_f.refresh_from_db()
        assert order_f.status == 'paid'

    def test_order_update_status_view_post_invalid_data(self, client,
                                                        order_update_url,
                                                        order_f):
        """Тест на обновление статуса заказа с невалидными данными"""
        data = {
            'status': '',
        }
        response = client.post(order_update_url, data)
        assert response.status_code == 200
        assert 'form' in response.context
        assert order_f.status != ''


@pytest.mark.django_db
class TestOrderDeleteView:
    def test_order_delete_view_get(self, client, order_delete_url, order_f):
        """Тест на получение страницы подтверждения удаления заказа"""
        response = client.get(order_delete_url)
        assert response.status_code == 200
        assert 'order' in response.context
        assert response.context['order'] == order_f

    def test_order_delete_view_post(self, client, order_delete_url, order_f):
        """Тест на удаление заказа"""
        response = client.post(order_delete_url)
        assert response.status_code == 302
        assert Order.objects.filter(id=order_f.id).count() == 0

    def test_order_delete_view_order_not_found(self, client):
        """Тест на получение страницы удаления заказа, если заказ не найден"""
        response = client.get(reverse('order_delete', args=[999]))
        assert response.status_code == 404
