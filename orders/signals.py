import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import Signal, receiver
from .models import Order

logger = logging.getLogger('orders')
order_was_created = Signal()


@receiver(post_save, sender=Order)
def log_order_saved(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Order created: ID {instance.id}, User: {instance.user.username}")
        order_was_created.send(sender=sender, order=instance)
    else:
        logger.info(f"Order updated: ID {instance.id}, User: {instance.user.username}")
        order_was_created.send(sender=sender, order=instance)


@receiver(post_delete, sender=Order)
def log_order_deleted(sender, instance, **kwargs):
    logger.warning(f"Order deleted: ID {instance.id}, User: {instance.user.username}")


@receiver(order_was_created)
def log_transaction_success(sender, order, **kwargs):
    try:
        logger.info(f"Transaction successful for order ID {order.id} by user {order.user.username}")
    except Exception as e:
        logger.error(f"Transaction failed for order ID {order.id}: {e}", exc_info=True)
