from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from dj.utils import log_action


@receiver([post_save, post_delete], dispatch_uid="log_model_changes")
def log_model_changes(sender, instance, created=None, **kwargs):
    """
    Receiver for post_save and post_delete signals to log model changes.
    """
    instance_id = getattr(instance, 'id', 'N/A')
    if created is not None:
        if created:
            log_action(
                'api', 'INFO',
                f'{sender.__name__} created: {instance}',
                id=instance_id
            )
        else:
            log_action(
                'api', 'INFO',
                f'{sender.__name__} updated: {instance}',
                id=instance_id
            )
    else:
        log_action(
            'api', 'INFO',
            f'{sender.__name__} deleted: {instance}',
            id=instance_id
        )
