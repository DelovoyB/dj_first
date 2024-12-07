import logging
from django.dispatch import Signal, receiver

page_viewed = Signal()

logger = logging.getLogger('main')


@receiver(page_viewed)
def log_page_view(sender, request, **kwargs):
    """
    Логгирует факт просмотра страницы.
    """
    user = request.user if request.user.is_authenticated else "Anonymous"
    logger.info(f"Page viewed: {request.path} by user {user}")
