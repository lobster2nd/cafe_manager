import pytest
from django.urls import reverse
from rest_framework import status

from manager_app.models import Order, MenuItem


@pytest.mark.django_db
class TestOrderViewSet:
    def test_create_order(self, client, menu_item, order_list_url):
        """Тест на создание заказа"""
        data = {
            "table_number": 1,
            "items": [menu_item.id]
        }
        response = client.post(order_list_url, data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        assert Order.objects.count() == 1
        assert Order.objects.get().table_number == 1

    def test_create_order_invalid_table_number(self, client, order_list_url):
        """Тест на создание заказа с недопустимым номером стола"""
        data = {
            "table_number": "invalid",
            "items": []
        }
        response = client.post(order_list_url, data, format='multipart')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Недопустимое значение" in response.data["error"]

    def test_retrieve_order(self, client, order_detail_url):
        """Тест на получение заказа по ID"""
        response = client.get(order_detail_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['table_number'] == 1

    def test_retrieve_order_not_found(self, client):
        """Тест на получение заказа, если он не найден"""
        response = client.get(reverse('orders-detail', args=[999]))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_partial_update_order(self, client, order, menu_item,
                                  order_detail_url):
        """Тест на частичное обновление заказа"""
        data = {
            "table_number": 2,
            "items": [menu_item.id]
        }
        response = client.patch(order_detail_url, data, format='multipart')
        assert response.status_code == status.HTTP_200_OK
        order.refresh_from_db()
        assert order.table_number == 2
        assert order.items.count() == 1

    def test_partial_update_order_item_not_found(self, client, order,
                                                 order_detail_url):
        """Тест на частичное обновление заказа с недопустимым пунктом меню"""
        data = {
            "table_number": 2,
            "items": [9]
        }
        response = client.patch(order_detail_url, data, format='multipart')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Пункт меню № 9 не найден." in response.data["detail"]

    def test_destroy_order(self, client, order, order_detail_url):
        """Тест на удаление заказа"""
        response = client.delete(order_detail_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Order.objects.count() == 0

    def test_destroy_order_not_found(self, client):
        """Тест на удаление заказа, если он не найден"""
        response = client.delete(reverse('orders-detail', args=[999]))
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestMenuItemViewSet:
    def test_create_menu_item(self, client, menu_item_list_url):
        """Тест на создание пункта меню"""
        data = {
            "name": "Burger",
            "price": 5.00
        }
        response = client.post(menu_item_list_url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert MenuItem.objects.count() == 1
        assert MenuItem.objects.get().name == "Burger"

    def test_create_menu_item_invalid(self, client, menu_item_list_url):
        """Тест на создание пункта меню с недопустимыми данными"""
        data = {
            "name": "",
            "price": -5.00
        }
        response = client.post(menu_item_list_url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Ошибка валидации" in response.data["error"]

    def test_list_menu_items(self, client, menu_item, menu_item_list_url):
        """Тест на получение списка пунктов меню"""
        response = client.get(menu_item_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == menu_item.name

    def test_list_menu_items_empty(self, client, menu_item_list_url):
        """Тест на получение списка пунктов меню, если их нет"""
        MenuItem.objects.all().delete()
        response = client.get(menu_item_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0
        assert response.data['results'] == []
