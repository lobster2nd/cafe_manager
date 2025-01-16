from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, \
    UpdateView, DeleteView

from manager_app.forms import AddOrderForm, AddMenuItemForm, OrderStatusForm
from manager_app.models import Order, MenuItem


class IndexPage(ListView):
    """Контроллер главной страницы со списком всех заказов"""
    model = Order
    template_name = "manager_app/index.html"
    context_object_name = "orders"
    print(Order.objects.last())


class AddOrderView(CreateView):
    """Создание нового заказа"""
    form_class = AddOrderForm
    template_name = "manager_app/add_order.html"
    success_url = reverse_lazy("home")
    raise_exception = True
    # order = Order.objects.last()
    # items = order.items.all()


class AddMenuItemView(CreateView):
    """Создание нового пункта меню"""
    form_class = AddMenuItemForm
    template_name = "manager_app/add_item.html"
    success_url = reverse_lazy("home")
    raise_exception = True


class OrderDetailView(DetailView):
    """Просмотр информации о заказе"""
    model = Order
    template_name = "manager_app/order_detail.html"
    context_object_name = "order"


class OrderUpdateStatus(UpdateView):
    """Редактирование статуса заказа"""
    model = Order
    form_class = OrderStatusForm
    template_name = "manager_app/update_order_status.html"

    def get_success_url(self):
        return reverse_lazy("order_detail", kwargs={"pk": self.object.pk})


class OrderDeleteView(DeleteView):
    """Удаление заказа"""
    model = Order
    template_name = "manager_app/order_confirm_delete.html"
    success_url = reverse_lazy("home")

