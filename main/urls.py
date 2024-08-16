from django.urls import path
from main.views import IndexView, AboutView, Index1View, About1View, ContactView, FaqView

app_name = 'main'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('index1/', Index1View.as_view(), name='index1'),
    path('about1/', About1View.as_view(), name='about1'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('faq/', FaqView.as_view(), name='faq'),
]