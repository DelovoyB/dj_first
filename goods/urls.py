from django.urls import path
from goods.views import ProductView, CatalogView, Catalog1View, Product1View

app_name = 'goods'
urlpatterns = [
    path('search/', CatalogView.as_view(), name='search'),
    path('new/search/', Catalog1View.as_view(), name='new_search'),
    path('<slug:category_slug>/', CatalogView.as_view(), name='index'),
    path('new/<slug:category_slug>/', Catalog1View.as_view(), name='index1'),
    path('product/<slug:product_slug>', ProductView.as_view(), name='product'),
    path('new/product/<slug:product_slug>', Product1View.as_view(), name='product1'),
]