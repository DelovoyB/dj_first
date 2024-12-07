from django.http import JsonResponse
from django.views import View

from carts.mixins import CartMixin
from carts.models import Cart
from goods.models import Products


class CartAddView(CartMixin, View):

    def post(self, request):
        """
        Add a product to the user's cart.

        Given a product ID from a POST request, either increase the quantity of a
        cart item if the product is already in the cart, or create a new cart item
        if the product is not in the cart.

        Returns a JSON response with a message and the HTML of the updated cart
        items.
        """
        product_id = request.POST.get("product_id")
        product = Products.objects.get(id=product_id)
        cart = self.get_cart(request, product=product)
        if cart:
            cart.quantity += 1
            cart.save()
        else:
            Cart.objects.create(user=request.user if request.user.is_authenticated else None,
                                session_key=request.session.session_key if not request.user.is_authenticated
                                else None,
                                product=product, quantity=1)

        response_data = {
            'message': 'Товар добавлен в корзину',
            'cart_items_html': self.render_cart(request),
        }

        return JsonResponse(response_data)


class CartChangeView(CartMixin, View):

    def post(self, request):
        """
        Change the quantity of a product in the user's cart.

        Given a product ID and new quantity from a POST request, update the
        quantity of the cart item. Returns a JSON response with a message, the
        new quantity, and the HTML of the updated cart items.
        """
        cart_id = request.POST.get("cart_id")

        cart = self.get_cart(request, cart_id=cart_id)
        cart.quantity = request.POST.get("quantity")
        cart.save()

        quantity = cart.quantity

        response_data = {
            'message': 'Количество изменено',
            'quantity': quantity,
            'cart_items_html': self.render_cart(request),
        }

        return JsonResponse(response_data)


class CartRemoveView(CartMixin, View):

    def post(self, request):
        """
        Remove a product from the user's cart.

        Given a cart ID from a POST request, delete the cart item and return a
        JSON response with a message, the quantity of the deleted item, and the
        HTML of the updated cart items.
        """
        cart_id = request.POST.get("cart_id")

        cart = self.get_cart(request, cart_id=cart_id)
        quantity = cart.quantity
        cart.delete()

        response_data = {
            'message': 'Товар удален из корзины',
            'quantity': quantity,
            'cart_items_html': self.render_cart(request),
        }

        return JsonResponse(response_data)
