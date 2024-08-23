from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def anonymous_required(view_func, redirect_url='user:profile'):
    return user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_url
    )(view_func)
