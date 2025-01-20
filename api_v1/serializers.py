from rest_framework import serializers

from manager_app.models import Order, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    """Сериализатор модели пункта меню"""
    class Meta:
        model = MenuItem
        fields = ["id", "name", "price"]

    def validate(self, attrs):
        name = attrs.get("name", "")
        price = attrs.get("price", "")
        if not name or not price:
            raise serializers.ValidationError()
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор модели заказа"""
    table_number = serializers.IntegerField(help_text="Номер столика")
    status = serializers.CharField(read_only=True, help_text="Статус")
    items = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(),
        many=True,
        help_text="Пункты меню"
    )
    total_price = serializers.IntegerField(help_text="Общая стоимость",
                                           read_only=True)

    class Meta:
        model = Order
        fields = ["id", "table_number", "items", "status", "total_price"]

    def to_representation(self, instance):
        """Метод для отображения полного представления пунктов меню"""
        representation = super().to_representation(instance)
        representation['items'] = MenuItemSerializer(instance.items.all(),
                                                     many=True).data
        representation['status'] = dict(Order.STATUS_CHOICES).get(
            instance.status, instance.status)
        return representation


class OrderStatusUpdateSerializer(OrderSerializer):
    """Сериализатор модели заказа для обновления заказа"""
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES,
                                     help_text="Статус заказа")

    def to_representation(self, instance):
        """Метод для отображения статуса в удобочитаемом виде"""
        representation = super().to_representation(instance)
        return representation

