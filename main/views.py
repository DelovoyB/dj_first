from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, ListView

from goods.models import Products


@method_decorator(cache_page(60 * 15), name='dispatch')
class IndexView(ListView):
    template_name = 'main/index.html'
    model = Products
    context_object_name = 'goods'

    def get_queryset(self):
        goods = super().get_queryset()

        self.hero1 = goods.filter(category__slug='smart-watches').first()
        self.hero2 = goods.filter(category__slug='headphones')[1]
        self.hero3 = goods.get(name="Apple iPhone 15 Pro Max")

        self.special1 = goods.filter(quantity__gt=0).order_by('-id')[:3]
        self.special2 = goods.filter(category__slug='headphones', discount__gt=0).first()
        self.special3 = goods.filter(category__slug='laptops').order_by('price').first()

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
