from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api_v1.views import OrderViewSet, MenuItemViewSet

router = DefaultRouter()

router.register('order', OrderViewSet, basename='orders')
router.register('menu_item', MenuItemViewSet, basename='menu_items')

urlpatterns = [
    path('', include(router.urls)),
]
