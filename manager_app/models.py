from django.db import models


class MenuItem(models.Model):
    """Модель пункта меню"""
    name = models.CharField(max_length=255,
                            verbose_name="Название блюда")
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name="Цена блюда")

    def __str__(self):
        return self.name


class Order(models.Model):
    """Модель заказа"""

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.PositiveIntegerField(verbose_name="номер стола")
    items = models.ManyToManyField(MenuItem,
                              verbose_name="Список заказанных блюд с ценами")
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='pending',
                              verbose_name="статус заказа")

    @property
    def total_price(self):
        """Свойство для вычисления общей суммы заказа"""
        return sum(item.price for item in self.items.all())

    def __str__(self):
        return (f"Order {self.pk} - Table {self.table_number} - "
                f"Status: {self.status}")

