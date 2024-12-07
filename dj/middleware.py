import logging
from django.http import Http404
import requests
from decouple import config

logger = logging.getLogger('django')

TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
CHAT_ID = '903899893'


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send Telegram message: {e}")


class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, Http404):
            logger.warning(f"Page not found: {request.path}")
            return None

        logger.error(f"Unhandled exception occurred: {exception}", exc_info=True)

        send_telegram_message(f"Unhandled exception occurred: {exception}")

        return None
