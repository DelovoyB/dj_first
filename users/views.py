import logging
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from carts.models import Cart
from common.mixins import CacheMixin
from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm

logger = logging.getLogger('users')


class UserLoginView(LoginView):

    template_name = 'users/login.html'
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        """
        Checks if the user is already authenticated and if the user is locked out.
        If locked out, returns an appropriate response.
        """
        if request.user.is_authenticated:
            return redirect(reverse_lazy('user:profile'))

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """
        Returns the URL that the user is redirected to after a successful login.

        If the user has provided a 'next' parameter in the request, it redirects to that URL.
        Otherwise, it redirects to the user's profile page.
        """
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page
        return reverse_lazy('user:profile')

    def form_valid(self, form):
        """
        If the form is valid, login the user and associate the user's carts with the user.

        If the user is logged in successfully, redirect to the user's profile page
        and send a success message to the user.
        """
        session_key = self.request.session.session_key

        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
                logger.info(f'User {user.username} logged in')
                messages.success(self.request, f'Вы успешно вошли в аккаунт {user.username}')
                return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        """
        Set the context data for the login page.

        Set the title of the page to "Sign in".
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign in'
        return context


class UserRegistrationView(CreateView):

    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:profile')

    def dispatch(self, request, *args, **kwargs):
        """
        Checks if the user is already authenticated. If yes, redirects to user profile,
        otherwise proceeds with the default dispatch method.
        """
        if request.user.is_authenticated:
            return redirect(reverse_lazy('user:profile'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Save the form data and log the user in.

        If the form is valid, it saves the form data, logs the user in, and
        updates any existing carts with the user's new ID. It then sends a
        success message to the user and redirects to the user profile page.
        """
        session_key = self.request.session.session_key

        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)
        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)
        logger.info(f'User {user.username} registered')
        messages.success(self.request, f'Вы успешно зарегистрировались {user.username}')
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        """
        Returns a dictionary with the given keyword arguments and the following
        additional context variables:

        *   title: The title of the page, which is 'Sign up'.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign up'
        return context


class UserProfileView(LoginRequiredMixin, CacheMixin, UpdateView):

    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('user:profile')

    def get_object(self, queryset=None):
        """
        Returns the user object associated with the current request.

        Returns:
            User: The user object associated with the current request.
        """
        return self.request.user

    def form_valid(self, form):
        """
        If the form is valid, send a success message to the user and call the
        form_valid method of the parent class to update the user profile.
        """
        logger.info(f'User {self.request.user.username} updated profile')
        messages.success(self.request, 'Профиль обновлен')
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        If the form is invalid, send an error message to the user and redirect
        back to the profile page with the invalid form.
        """
        logger.warning(f'User {self.request.user.username} failed to update profile')
        messages.error(self.request, 'Профиль не обновлен')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Set the context data for the user profile page.

        The context data includes the page title, and the user's orders.

        Returns:
            dict: The context data for the user profile page.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile'
        orders = Order.objects.filter(user=self.request.user).prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )).order_by("-id")

        context['orders'] = self.set_get_cache(orders, f'user_{self.request.user.id}_orders', 60)
        logger.info(f"{self.request.user.username}'s orders are cached")
        return context


class UserCartView(TemplateView):

    template_name = 'users/users_cart.html'

    def get_context_data(self, **kwargs):
        """
        Set the context data for the user cart page.

        The context data includes the page title, whether the page is a cart page, and
        whether to disable the modal cart.

        Returns:
            dict: The context data for the user cart page.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cart'
        context['disable_modal_cart'] = True

        return context


@login_required
def logout(request):
    """
    Logout the user and redirect to the main page.

    This view is protected by the @login_required decorator, so
    only authenticated users can access it.

    After logging out, a success message is sent to the user,
    and they are redirected to the main page.
    """
    logger.info(f'User {request.user.username} logged out')
    messages.success(request, 'Вы вышли из аккаунта')
    auth.logout(request)
    return redirect(reverse('main:index'))
