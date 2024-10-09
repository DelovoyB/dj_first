from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from common.mixins import CacheMixin
from goods.models import Products


class IndexView(CacheMixin, ListView):
    template_name = 'main/index.html'
    model = Products
    context_object_name = 'goods'
    cache_time = 60 * 15

    def get_queryset(self):
        """
        Override get_queryset to set hero and special products to the instance
        variables. These are then used in the get_context_data method to be
        added to the context.

        Returns the queryset of all products.
        """
        goods = super().get_queryset()

        self.hero1 = self.set_get_cache_fn(
            'hero1_cache',
            lambda: goods.filter(category__slug='smart-watches').first(),
            self.cache_time
        )
        self.hero2 = self.set_get_cache_fn(
            'hero2_cache',
            lambda: goods.filter(category__slug='headphones')[1],
            self.cache_time
        )
        self.hero3 = self.set_get_cache_fn(
            'hero3_cache',
            lambda: goods.get(name="Apple iPhone 15 Pro Max"),
            self.cache_time
        )

        self.special1 = self.set_get_cache_fn(
            'special1_cache',
            lambda: list(goods.filter(quantity__gt=0).order_by('-id')[:3]),
            60*3
        )

        self.special2 = self.set_get_cache_fn(
            'special2_cache',
            lambda: goods.filter(category__slug='headphones', discount__gt=0).first(),
            self.cache_time
        )

        self.special3 = self.set_get_cache_fn(
            'special3_cache',
            lambda: goods.filter(category__slug='laptops').order_by('price').first(),
            self.cache_time
        )

        return goods

    def get_context_data(self, **kwargs):
        """
        Set the context data for the main page.

        Set the title of the page to "Main page", and set the context variables
        hero1, hero2, hero3, special1, special2, and special3 to the corresponding
        products.

        Returns:
            dict: The context data for the main page.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Main page'
        context['hero1'] = self.hero1
        context['hero2'] = self.hero2
        context['hero3'] = self.hero3
        context['special1'] = self.special1
        context['special2'] = self.special2
        context['special3'] = self.special3
        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        """
        Set the context data for the about page.

        Set the title of the page to "About us".

        Returns:
            dict: The context data for the about page.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'About us'
        return context


class ContactView(TemplateView):
    template_name = 'main/contact.html'

    def get_context_data(self, **kwargs):
        """
        Set the context data for the contact page.

        Set the title of the page to "Contact us".

        Returns:
            dict: The context data for the contact page.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact us'
        return context


class FaqView(TemplateView):
    template_name = 'main/faq.html'

    def get_context_data(self, **kwargs):
        """
        Set the context data for the FAQ page.

        Set the title of the page to "FAQ".

        Returns:
            dict: The context data for the FAQ page.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'FAQ'
        return context


def handle404(request, exception):
    """
    A custom 404 handler that renders the 404.html template with a status code of 404.

    Args:
        request (Request): The request object.
        exception (Exception): The exception that caused the 404 error.

    Returns:
        Response: The rendered 404.html template with a status code of 404.
    """
    return render(request, 'main/404.html', status=404)
