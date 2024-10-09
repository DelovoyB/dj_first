import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj.settings')

app = Celery('dj')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """
    A simple task that prints its request to the console.

    Useful for testing and debugging Celery configurations.

    """
    print(f'Request: {self.request!r}')
