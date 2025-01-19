from django.urls import path, include

from .views import *

urlpatterns = [
    path("", OrderListView.as_view(), name="home"),
    path("order/add/", AddOrderView.as_view(), name="add_order"),
    path("item/add/", AddMenuItemView.as_view(), name="add_item"),
    path("order/detail/<int:pk>/", OrderDetailView.as_view(),
         name="order_detail"),
    path("order/update/<int:pk>/", OrderUpdateStatus.as_view(),
         name="order_edit"),
    path("order/delete/<int:pk>/", OrderDeleteView.as_view(),
         name="order_delete"),
    path("total_revenue/", RevenueView.as_view(), name="total_revenue"),
]
