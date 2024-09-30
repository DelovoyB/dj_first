from django.db import models

from users.models import User
from goods.models import Products


class CartQueryset(models.QuerySet):

    def total_price(self):
        """
        Returns the total price of all items in the cart.
        """
        return sum(cart.products_price() for cart in self)


    def total_quantity(self):
        """
        Returns the total quantity of all items in the cart.
        If the cart is empty, it returns 0.
        """
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    session_key = models.CharField(max_length=32, blank=True, null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart'
        ordering = ('-created_timestamp',)

    objects = CartQueryset().as_manager()

    def products_price(self):
        """
        Returns the total price of all items in the cart.

        Returns:
            float: The total price of all items in the cart.
        """
        return round(self.product.sell_price() * self.quantity,2)

    def __str__(self):
        """
        Returns a string representation of the cart object.

        If the cart is for an authenticated user, it will include the user's username
        and the product name. If the cart is for an anonymous user, it will just include
        the product name and quantity.

        Returns:
            str: A string representation of the cart object.
        """       
        if self.user:
            return f'Cart for {self.user.username} | Product {self.product.name} | Quantity {self.quantity}'

        return f'Anonymous user | Product {self.product.name} | Quantity {self.quantity}'