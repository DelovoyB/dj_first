from django.template.loader import render_to_string
from django.urls import reverse

from carts.models import Cart
from carts.utils import get_user_carts


class CartMixin:

    def get_cart(self, request, product=None, cart_id=None):
        """
        Get a cart object, either by product or id, or get a user's cart object if not specified.

        Args:
            request (Request): The request object to check if the user is authenticated.
            product (Products, optional): The product to get the cart for. Defaults to None.
            cart_id (int, optional): The id of the cart to get. Defaults to None.

        Returns:
            Cart: The cart object that matches the given criteria, or None if no match is found.
        """
        if request.user.is_authenticated:
            query_kwargs = {'user': request.user}
        else:
            query_kwargs = {'session_key': request.session.session_key}

        if product:
            query_kwargs['product'] = product

        if cart_id:
            query_kwargs['id'] = cart_id

        return Cart.objects.filter(**query_kwargs).first()

    def render_cart(self, request):
        """
        Render the cart template with the given request object.

        Args:
            request (Request): The request object to get the cart items for.

        Returns:
            str: The rendered template as a string.
        """
        user_cart = get_user_carts(request)
        context = {'carts': user_cart}

        referer = request.META.get('HTTP_REFERER')
        if reverse('orders:create_order') in referer:
            context['order'] = True

        return render_to_string('carts/includes/included_cart.html', context, request=request)