from django.contrib import admin

from carts.admin import CartTabAdmin
from orders.admin import OrderTabularAdmin
from users.models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ('username', 'email')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    inlines = [CartTabAdmin, OrderTabularAdmin]