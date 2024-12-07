import logging
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.forms import ValidationError
from django.urls import reverse_lazy
from django.views.generic import FormView

from .tasks import send_order_email, task1 # noqa
from .signals import order_was_created

from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem

logger = logging.getLogger('orders')


class CreateOrderView(LoginRequiredMixin, FormView):

    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('user:profile')

    def get_initial(self):
        """
        Return the initial data for the form.

        The initial data is set as follows:

        - first_name: The first name of the current user.
        - last_name: The last name of the current user.

        The initial data is then passed to the form to be used as the initial values of the form fields.
        """
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        return initial

    def form_valid(self, form):
        """
        If the form is valid, create a new order and order items based on the
        items in the cart and the form data.

        If there is not enough stock for a product in the cart, raise a
        ValidationError. If there is enough stock, create a new order item and
        deduct the quantity of the order item from the product's quantity.

        After the order is created, send an email to the user with the order
        details.

        If there is an error creating the order, return a redirect to the create
        order view with a warning message.
        """
        try:
            with transaction.atomic():
                user = self.request.user
                cart = Cart.objects.filter(user=user).select_related('product')

                order = Order.objects.create(
                    user=user,
                    phone_number=form.cleaned_data['phone_number'],
                    requires_delivery=form.cleaned_data['requires_delivery'],
                    delivery_address=form.cleaned_data['delivery_address'],
                    payment_on_get=form.cleaned_data['payment_on_get'],
                )

                for cart_item in cart:
                    product = cart_item.product
                    name = cart_item.product.name
                    price = cart_item.product.sell_price()
                    quantity = cart_item.quantity

                    if product.quantity < quantity:
                        raise ValidationError(f'Недостаточное количество {name} в наличии')

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        name=name,
                        price=price,
                        quantity=quantity
                    )

                    product.quantity -= quantity
                    product.save()

                    cart_item.delete()

                order_was_created.send(sender=Order, order=order)
                transaction.on_commit(lambda: task1(order.id, user.email))
                return redirect('user:profile')

        except ValidationError as error:
            logger.error(f"Failed to process order for user {self.request.user.username}: {error}", exc_info=True)
            return redirect('orders:create_order')

    def form_invalid(self, form):
        """
        If the form is invalid, redirect back to the checkout page with
        an error message.
        """
        messages.error(self.request, 'Заполните все обязательные поля')
        return redirect('orders:create_order')

    def get_context_data(self, **kwargs):
        """
        Set the context data for the checkout page.

        The context data includes the page title, whether the page is an order
        page, and whether to disable the modal cart.

        Returns:
            dict: The context data for the checkout page.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Checkout'
        context['order'] = True
        context['disable_modal_cart'] = True
        return context
