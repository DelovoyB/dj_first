from django.dispatch import receiver, Signal
import logging

logger = logging.getLogger('goods')

product_list_viewed = Signal()
product_detail_viewed = Signal()


@receiver(product_list_viewed)
def log_product_list_view(sender, user, filters=None, **kwargs):
    logger.info(f"Product list viewed by user {user}. Filters: {filters}")


@receiver(product_detail_viewed)
def log_product_detail_view(sender, user, product=None, **kwargs):
    if product:
        logger.info(f"Product '{product.slug}' viewed by user {user}")
    else:
        logger.warning(f"Product '{kwargs.get('path')}' not found for user {user}")
