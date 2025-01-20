from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, \
    HTTP_201_CREATED, HTTP_204_NO_CONTENT
from django_filters import rest_framework as filters

from api_v1.filters import OrderFilter
from api_v1.serializers import OrderSerializer, MenuItemSerializer, \
    OrderStatusUpdateSerializer
from api_v1.swagger_responses import response_400, response_404
from manager_app.models import Order, MenuItem


class OrderViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                   mixins.ListModelMixin, mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    """Работа с заказами"""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    ordering = ["table_number",]
    parser_classes = (MultiPartParser, FormParser)

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrderFilter

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от типа запроса"""
        if self.request.method == 'PATCH':
            return OrderStatusUpdateSerializer
        return OrderSerializer

    def list(self, request, *args, **kwargs):
        """
        Получить список всех заказов

        Получить список всех заказов
        """
        return super().list(request, args, kwargs)

    @swagger_auto_schema(
        responses={400: response_400,
                   404: response_404})
    def create(self, request, *args, **kwargs):
        """
        Добавить заказ

        Добавить заказ
        """

        table_number = request.data.get("table_number")

        if not isinstance(table_number, int):
            return Response({"error": "Недопустимое значение"},
                            status=HTTP_400_BAD_REQUEST)

        order = Order(table_number=table_number)
        order.save()

        items_data = request.data.get("items", [])

        for item_id in items_data:
            if item_id != ",":
                menu_item = (MenuItem.objects
                             .filter(id=int(item_id))
                             .first())
                if not menu_item:
                    return Response(
                        {
                            "detail": f"Пункт меню № {item_id} не найден."},
                        status=HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={404: response_404})
    def retrieve(self, request, *args, **kwargs):
        """
        Получить заказ по id

        Получить заказ по id
        """
        try:
            instance = self.get_object()
        except Http404:
            raise NotFound(detail="Заказ не найден.")
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={400: response_400,
                   404: response_404})
    def partial_update(self, request, *args, **kwargs):
        """
        Обновить заказ

        Обновить заказ
        """
        try:
            instance = self.get_object()
        except Http404:
            raise NotFound(detail="Заказ не найден.")

        table_number = request.data.get("table_number")
        items_data = request.data.get("items", [])
        status = request.data.get("status")

        if status is not None:
            instance.status = status

        if table_number is not None:
            instance.table_number = table_number

            instance.items.clear()

            for item_id in items_data:
                if item_id and item_id != ",":
                    menu_item = (MenuItem.objects
                                 .filter(id=int(item_id))
                                 .first())
                    if not menu_item:
                        return Response(
                            {
                                "detail": f"Пункт меню № {item_id} не найден."},
                            status=HTTP_404_NOT_FOUND)
                    else:
                        instance.items.add(menu_item)

        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={404: response_404})
    def destroy(self, request, *args, **kwargs):
        """
        Удалить заказ по ID

        Удалить заказ по ID
        """
        try:
            instance = self.get_object()
        except Http404:
            raise NotFound(detail="Заказ не найден.")

        instance.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class MenuItemViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """Работа с пунктами меню"""

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering = ["name", ]

    @swagger_auto_schema(
        responses={400: response_400})
    def create(self, request, *args, **kwargs):
        """
        Добавить пункт меню

        Добавить пункт меню
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            menu_item = serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=HTTP_201_CREATED,
                            headers=headers)

        except ValidationError:
            return Response({"error": "Ошибка валидации"},
                            status=HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        Получить список всех пунктов меню

        Получить список всех пунктов меню
        """
        return super().list(request, args, kwargs)
