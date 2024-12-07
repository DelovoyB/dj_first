from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from dj.utils import log_action
from carts.models import Cart


@receiver(post_save, sender=Cart)
def log_cart_save(sender, instance, created, **kwargs):
    """
    Receiver for post_save signals to log cart saves.
    """
    if created:
        log_action(
            'carts',
            'INFO',
            f'Cart created: {instance}',
            id=instance.id
        )
    else:
        log_action(
            'carts',
            'INFO',
            f'Cart updated: {instance}',
            id=instance.id
        )


@receiver(post_delete, sender=Cart)
def log_cart_delete(sender, instance, **kwargs):
    """
    Receiver for post_delete signals to log cart deletions.
    """
    log_action(
        'carts',
        'INFO',
        f'Cart deleted: {instance}',
        id=instance.id
    )
