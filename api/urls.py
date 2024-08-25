from django.urls import path
from api import views

app_name = 'api'
urlpatterns = [
    path('users/all/', views.UsersList.as_view(), name='users_list'),
    path('users/<str:username>/', views.UsersRetrieveUpdateDestroy.as_view(), name='users_retrieve_update_destroy'),

    path('categories/all/', views.CategoriesList.as_view(), name='categories_list'),
    path('categories/<str:slug>/', views.CategoriesRetrieveUpdateDestroy.as_view(), name='categories_retrieve_update_destroy'),

    path('products/all/', views.ProductsList.as_view(), name='products_list'),
    path('products/<str:slug>/', views.ProductsRetrieveUpdateDestroy.as_view(), name='products_retrieve_update_destroy'),

    path('orders/all/', views.OrdersList.as_view(), name='orders_list'),
    path('orders/<int:id>/', views.OrdersRetrieveUpdateDestroy.as_view(), name='orders_retrieve_update_destroy'),
]