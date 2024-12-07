import logging
from django.http import Http404
from django.views.generic import DetailView, ListView

from common.mixins import CacheMixin
from goods.models import Products
from goods.utils import q_search

from .signals import product_list_viewed, product_detail_viewed

logger = logging.getLogger('goods')


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
            goods = super().get_queryset().select_related('category')
        elif query:
            goods = q_search(query)
            if not goods.exists():
                logger.warning(f"Page not found: {self.request.path}?q={query} by user {self.request.user}")
                raise Http404()
        else:
            goods = super().get_queryset().filter(category__slug=category_slug).select_related('category')
            if not goods.exists():
                logger.warning(f"Page not found: {self.request.path} by user {self.request.user}")
                raise Http404()

        if on_sale:
            goods = goods.filter(discount__gt=0)

        if order_by and order_by != 'default':
            goods = goods.order_by(order_by)

        product_list_viewed.send(
            sender=self.__class__,
            user=self.request.user,
            filters=query if query else category_slug,
        )

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
        try:
            product = self.set_get_cache_fn(
                f'goods_product_{self.kwargs["product_slug"]}',
                lambda: Products.objects.select_related('category').get(slug=self.kwargs["product_slug"]),
                30
            )

            product_detail_viewed.send(
                sender=self.__class__,
                user=self.request.user,
                product=product,
            )
            return product

        except Products.DoesNotExist:
            product_detail_viewed.send(
                sender=self.__class__,
                user=self.request.user,
                product=None,
                path=self.request.path
            )
            raise Http404()

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
