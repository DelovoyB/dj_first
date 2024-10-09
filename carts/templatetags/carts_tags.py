from django import template

from carts.utils import get_user_carts

register = template.Library()


@register.simple_tag()
def user_carts(request):
    """
    Template tag to get a user's carts.

    This tag takes a request object and returns a QuerySet of Cart objects related to the user.

    Returns:
        QuerySet of Cart objects
    """
    return get_user_carts(request)
