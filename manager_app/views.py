from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, \
    UpdateView, DeleteView, TemplateView

from manager_app.forms import AddOrderForm, AddMenuItemForm, OrderStatusForm
from manager_app.models import Order


class OrderListView(ListView):
    """Контроллер главной страницы со списком всех заказов"""
    model = Order
    template_name = "manager_app/index.html"
    context_object_name = "orders"
    paginate_by = 3

    def get_queryset(self):
        """Метод фильтрации для поиска по номеру стола и статусу"""
        queryset = super().get_queryset()

        table_number_query = self.request.GET.get('table_number')
        status_query = self.request.GET.get('status')

        if table_number_query:
            queryset = queryset.filter(
                table_number__icontains=table_number_query)

        if status_query:
            queryset = queryset.filter(
                status=status_query)

        return queryset


class AddOrderView(CreateView):
    """Создание нового заказа"""
    form_class = AddOrderForm
    template_name = "manager_app/add_order.html"
    success_url = reverse_lazy("home")
    raise_exception = True


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


class RevenueView(TemplateView):
    """Страница для расчета общего объема выручки за оплаченные заказы"""
    template_name = "manager_app/revenue.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paid_orders = Order.objects.filter(status='paid')

        total_revenue = sum(order.total_price for order in paid_orders)

        context['total_revenue'] = total_revenue
        return context
