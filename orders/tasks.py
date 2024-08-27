from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from orders.models import Order


@shared_task
def send_order_email(order_id, user_email):
    try:
        order = Order.objects.get(id=order_id)

        subject = f'Order confirmation No {order.id}'
        message = f'Thanks for your order. Your order No {order.id} is being processed.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user_email]

        send_mail(subject, message, email_from, recipient_list)

    except Exception as e:
        with open('lg_error.log', 'w') as f:
            f.write(f"Error: {str(e)}\n")
        raise


@shared_task
def task1():
    print('task1')
    return "OK"
