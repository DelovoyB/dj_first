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
            self.cache_time
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
        context = super().get_context_data(**kwargs)
        context['title'] = 'Main page'
        context['hero1'] = self.hero1
        context['hero2'] = self.hero2
        context['hero3'] = self.hero3
        context['special1'] = self.special1
        context['special2'] = self.special2
        context['special3'] = self.special3
        return context

# class IndexView(CacheMixin, ListView):
#     template_name = 'main/index.html'
#     model = Products
#     context_object_name = 'goods'
#     cache_time = 60 * 15
#
#     def get_queryset(self):
#         goods = super().get_queryset()
#
#         self.hero1 = self.set_get_cache(goods.filter(category__slug='smart-watches').first(), 'hero1_cache', self.cache_time)
#         self.hero2 = self.set_get_cache(goods.filter(category__slug='headphones')[1], 'hero2_cache', self.cache_time)
#         self.hero3 = self.set_get_cache(goods.get(name="Apple iPhone 15 Pro Max"), 'hero3_cache', self.cache_time)
#
#         self.special1 = self.set_get_cache(list(goods.filter(quantity__gt=0).order_by('-id')[:3]), 'special1_cache', self.cache_time)
#         self.special2 = self.set_get_cache(goods.filter(category__slug='headphones', discount__gt=0).first(), 'special2_cache', self.cache_time)
#         self.special3 = self.set_get_cache(goods.filter(category__slug='laptops').order_by('price').first(), 'special3_cache', self.cache_time)
#
#         return goods
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Main page'
#         context['hero1'] = self.hero1
#         context['hero2'] = self.hero2
#         context['hero3'] = self.hero3
#         context['special1'] = self.special1
#         context['special2'] = self.special2
#         context['special3'] = self.special3
#         return context


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About us'
        return context


class ContactView(TemplateView):
    template_name = 'main/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact us'
        return context


class FaqView(TemplateView):
    template_name = 'main/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'FAQ'
        return context


def handle404(request, exception):
    return render(request, 'main/404.html', status=404)


# def about(request):
#     context = {
#         'title': 'О нас'
#     }
#     return render(request, 'main/about.html', context)
