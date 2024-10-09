from carts.models import Cart


def get_user_carts(request):
    """
    Get a user's carts from the database.

    If the user is authenticated, we query the database with the user's id.
    If the user is not authenticated, we query the database with the session key.
    If the session key doesn't exist yet, we create it.

    Returns a QuerySet of Cart objects related to the user.
    """
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).select_related('product')

    if not request.session.session_key:
        request.session.create()
    return Cart.objects.filter(session_key=request.session.session_key).select_related('product')
