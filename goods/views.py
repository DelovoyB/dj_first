from django.http import Http404
from django.views.generic import DetailView, ListView

from common.mixins import CacheMixin
from goods.models import Products
from goods.utils import q_search


class CatalogView(ListView):
    model = Products
    template_name = 'goods/catalog.html'
    context_object_name = 'goods'
    paginate_by = 6
    allow_empty = False

    def get_queryset(self):
        """
        Returns a filtered queryset of Products based on the given request
        parameters.

        *   If the category_slug parameter is 'all', it returns all products.
        *   If the q parameter is given, it performs a full-text search on the
            product name and description.
        *   Otherwise, it filters the products by the given category slug.
        *   If the on_sale parameter is given, it filters the products that have
            a discount greater than zero.
        *   If the order_by parameter is given, it sorts the products by the
            given field name.

        If the filtered queryset is empty, it raises a 404 error.

        Returns:
            QuerySet: A filtered queryset of Product objects.
        """
        category_slug = self.kwargs.get('category_slug')
        on_sale = self.request.GET.get('on_sale')
        order_by = self.request.GET.get('order_by')
        query = self.request.GET.get('q')

        if category_slug == 'all':
            goods = super().get_queryset()
        elif query:
            goods = q_search(query)
        else:
            goods = super().get_queryset().filter(category__slug=category_slug)
            if not goods.exists():
                raise Http404()

        if on_sale:
            goods = goods.filter(discount__gt=0)

        if order_by and order_by != 'default':
            goods = goods.order_by(order_by)

        return goods

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Returns a dictionary with the given keyword arguments and the following
        additional context variables:
    
        *   title: The title of the page, which is 'Shop'.
        *   slug_url: The slug of the category given in the URL parameters.
    
        Returns:
            dict: A dictionary with the additional context variables.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Shop'
        context["slug_url"] = self.kwargs.get('category_slug')
        return context


class ProductView(CacheMixin, DetailView):

    template_name = 'goods/product.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        """
        Returns a Product object by slug from the URL parameters.
        
        The product is retrieved from the cache if it exists, otherwise it is
        retrieved from the database and cached for 30 seconds.
        
        Returns:
            Product: The product object with the given slug.
        """
        product = self.set_get_cache_fn(
            f'goods_product_{self.kwargs['product_slug']}',
            lambda: Products.objects.get(slug=self.kwargs['product_slug']),
            30
        )
        return product

    def get_context_data(self, **kwargs):
        """
        Returns a dictionary with the given keyword arguments and the following
        additional context variables:

        *   title: The title of the page, which is the name of the product.

        Returns:
            dict: A dictionary with the additional context variables.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context
