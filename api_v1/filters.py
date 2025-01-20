from django_filters import rest_framework as filters

from manager_app.models import Order


class OrderFilter(filters.FilterSet):
    """Фильтр для модели заказа"""
    table_number = filters.NumberFilter(field_name='table_number',
                                        lookup_expr='exact')
    status = filters.ChoiceFilter(field_name='status',
                                  choices=Order.STATUS_CHOICES)

    class Meta:
        model = Order
        fields = ['table_number', 'status']