from django import template
from django.utils.http import urlencode

from goods.models import Categories

register = template.Library()


@register.simple_tag
def tag_categories():
    """
    Returns a list of all categories.

    Example usage in template:
    {% for category in tag_categories %}
        {{ category }}
    {% endfor %}
    """
    return Categories.objects.all()


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    """
    Returns a URL-encoded string of the current request's query parameters
    updated with the given keyword arguments.

    Example usage in template:
    <a href="?{% change_params category='1' %}">Category 1</a>
    """
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
