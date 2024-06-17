from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404

from goods.models import Products, Categories


# Create your views here.

def catalog(request, category_slug, page=1):

    if category_slug == 'all':
        goods = Products.objects.all()
    else:
        category = Categories.objects.get(slug=category_slug)
        goods = get_list_or_404(Products.objects.filter(category=category))

    paginator = Paginator(goods, 3)
    current_page = paginator.page(page)

    context = {
        'title':'Каталог',
        'goods':current_page,
        'slug_url':category_slug,
    }
    return render(request, 'goods/catalog.html', context)

def product(request, slug):

    product = Products.objects.get(slug=slug)

    context = {
        'title':product.name,
        'product':product,
    }

    return render(request, 'goods/product.html', context=context)