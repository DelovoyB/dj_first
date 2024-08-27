from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.forms import ValidationError
from django.urls import reverse_lazy
from django.views.generic import FormView

from .tasks import send_order_email

from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


class CreateOrderView(LoginRequiredMixin, FormView):

    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('user:profile')

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
                cart = Cart.objects.filter(user=user)

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

                messages.success(self.request, 'Заказ успешно оформлен')
                transaction.on_commit(lambda: send_order_email(order.id, user.email))
                return redirect('user:profile')

        except ValidationError as error:
            messages.warning(self.request, error.message)
            return redirect('orders:create_order')

    def form_invalid(self, form):
        messages.error(self.request, 'Заполните все обязательные поля')
        return redirect('orders:create_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Checkout'
        context['order'] = True
        context['disable_modal_cart'] = True
        return context
