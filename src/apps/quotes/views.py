import json

import logging
from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.http import JsonResponse

from django.views import View

from nemodev_platform import settings
from src.apps.quotes.telegram_bot_processor import get_processor

from src.base.view.log import LogMixin
from src.base.view.permission import CSRFExemptInMixin


common_log = logging.getLogger('common_log')


class QuoteTelegramBotView(CSRFExemptInMixin, LogMixin, View):

    def __init__(self, **kwargs):
        super(QuoteTelegramBotView, self).__init__(**kwargs)

    def get_log_name(self):
        return 'telegram_quote_bot_log'

    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid bot token!')

        try:
            user_message = json.loads(request.body.decode('utf-8'), 'utf-8')
        except ValueError:
            return HttpResponseBadRequest('Invalid request body!')

        common_log.info(msg=str(user_message))
        processor = get_processor(user_message)
        if processor:
            processor.process()

        return JsonResponse({}, status=200)
