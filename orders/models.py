from django.db import models

from goods.models import Products
from users.models import User


class OrderitemQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Order(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    requires_delivery = models.BooleanField(default=False)
    delivery_address = models.TextField(blank=True, null=True)
    payment_on_get = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='Processing')

    class Meta:
        db_table = 'order'
        ordering = ('-created_timestamp',)

    def __str__(self):
        return f'Order ID {self.pk} | Buyer {self.user.first_name} {self.user.last_name}'


class OrderItem(models.Model):

    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Products, on_delete=models.SET_DEFAULT, null=True,default=None)
    name = models.CharField(max_length=150)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_item'
        ordering = ('id',)

    objects = OrderitemQueryset.as_manager()

    def products_price(self):
        return round(self.price * self.quantity, 2)

    def __str__(self):
        return f'Product {self.name} | Order ID {self.order.pk}'