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

        if obj.user:
            return obj.user
        return "Анонимный пользователь"


    def product_display(self, obj):

        return str(obj.product.name)

    user_display.short_description = 'Пользователь'
    product_display.short_description = 'Товар'
