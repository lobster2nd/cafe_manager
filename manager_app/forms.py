from django import forms

from manager_app.models import Order, MenuItem


class AddOrderForm(forms.ModelForm):
    """Форма создания заказа"""
    class Meta:
        model = Order
        fields = ["table_number", "items"]


class AddMenuItemForm(forms.ModelForm):
    """Форма создания пункта меню"""
    class Meta:
        model = MenuItem
        fields = ["name", "price"]


class OrderStatusForm(forms.ModelForm):
    """Форма обновления статуса заказа"""
    class Meta:
        model = Order
        fields = ['status']
