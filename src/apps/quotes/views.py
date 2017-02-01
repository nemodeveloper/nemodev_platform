import json

import telepot
from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.http import JsonResponse


# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from nemodev_platform import settings
from src.apps.quotes.models import Quote


# QuoteTelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)
# QuoteTelegramBot.setWebhook('https://bot.khashtamov.com/planet/bot/%s/' % settings.TELEGRAM_BOT_TOKEN)


class QuoteTelegramBotView(View):

    def __init__(self, **kwargs):
        super(QuoteTelegramBotView, self).__init__(**kwargs)
        self.commands = {
            '/start': '',
            '/help': '',
            '/quote': QuoteTelegramBotView._get_random_quote,
        }

    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid bot token!')

        try:
            user_message = json.loads(request.body.decode('utf-8'), 'utf-8')
        except ValueError:
            return HttpResponseBadRequest('Invalid request body!')

        chat_id = user_message['message']['chat']['id']
        cmd = user_message['message'].get('text')

        func = self.commands.get(cmd.split()[0].lower())
        # if func:
        #     TelegramBot.sendMessage(chat_id, func(), parse_mode='Markdown')
        # else:
        #     TelegramBot.sendMessage(chat_id, 'I do not understand you, Sir!')

        return JsonResponse({'text': func()}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(QuoteTelegramBotView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def _get_random_quote(cls):
        return Quote.quote_manager.get_random_quotes(1)[0].text
