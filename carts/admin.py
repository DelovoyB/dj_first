from django.contrib import admin

from carts.models import Cart


class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = 'product', 'quantity', 'created_timestamp'
    search_fields = 'product', 'quantity', 'created_timestamp'
    readonly_fields = ('created_timestamp',)
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = ['user_display', 'product_display', 'quantity', 'created_timestamp']
    list_filter = ['user', 'product__name', 'created_timestamp']
    search_fields = ['user']

    def user_display(self, obj):
        """
        Return the user associated with the cart, or "Anonymous user" if the
        cart is anonymous.
        """
        if obj.user:
            return obj.user
        return "Anonymous user"


    def product_display(self, obj):
        """
        Return the name of the product associated with the cart.
        """
        return str(obj.product.name)

    user_display.short_description = 'User'
    product_display.short_description = 'Product'
