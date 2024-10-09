from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ProductViewSet, UserViewSet, CategoryViewSet, OrderViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)
router.register('orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
