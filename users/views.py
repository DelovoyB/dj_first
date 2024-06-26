from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.decorators import anonymous_required
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm


# Create your views here.
@anonymous_required
def login(request):

    # if request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('user:profile'))
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, f'Вы успешно вошли в аккаунт {username}')
                if request.POST.get('next'):
                    return HttpResponseRedirect(request.POST['next'])
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()

    context = {
        'title' : 'Авторизация',
        'form' : form,
    }
    return render(request, 'users/login.html', context)

# @anonymous_required
def registration(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:profile'))
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success(request, f'Вы успешно зарегистрировались {user.username}')
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context = {
        'title' : 'Регистрация',
        'form' : form,
    }
    return render(request, 'users/registration.html', context)

@login_required
def profile(request):

    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль успешно обновлен')
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)

    context = {
        'title' : 'Кабинет',
        'form' : form,
    }
    return render(request, 'users/profile.html', context)

@login_required
def logout(request):
    messages.success(request, 'Вы вышли из аккаунта')
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))

def users_cart(request):
    return render(request, 'users/users_cart.html')