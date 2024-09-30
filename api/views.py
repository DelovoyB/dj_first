from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from api.serializer import UserSerializer, CategorySerializer, ProductSerializer, OrderSerializer
from goods.models import Categories, Products
from orders.models import Order
from users.models import User


@method_decorator(cache_page(30), name='dispatch')
class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Override get_permissions to only return IsAuthenticated for list and retrieve actions
        and IsAuthenticated and IsAdminUser for other actions.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Override get_queryset to only return all users if the current user is staff
        
        Otherwise, return an empty queryset.
        """
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.none()
        return queryset


@method_decorator(cache_page(30), name='dispatch')
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


@method_decorator(cache_page(30), name='dispatch')
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


@method_decorator(cache_page(30), name='dispatch')
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'
