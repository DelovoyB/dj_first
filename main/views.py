from django.shortcuts import render
from django.http import HttpResponse

from goods.models import Categories

# Create your views here.
def index(request):
    context = {
        'title': 'Главная',
        'content': 'Магазин мебели HOME',
    }
    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'title': 'О нас'
    }
    return render(request, 'main/about.html', context)
