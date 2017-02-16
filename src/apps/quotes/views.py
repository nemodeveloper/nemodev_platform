import json

import logging
import telepot
from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.views import View

from nemodev_platform import settings
from src.apps.quotes.models import Quote, Category

from src.base.view.log import LogViewMixin
from src.base.view.permission import CSRFExemptInMixin


common_log = logging.getLogger('common_log')

QuoteTelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)
QuoteTelegramBot.setWebhook('https://quotesformuse.ru/quotes/bot/%s/' % settings.TELEGRAM_BOT_TOKEN)


def filter_category(func):
    def temp(*args, **kwargs):
        if args[1]:
            raw_category = args[1][0].lower().title()
            category = Category.objects.filter(name__startswith=raw_category).first()
            if category:
                return func(args[0], category)
        return 'К сожалению мне не удалось ничего найти по запросу %s' % ' '.join(args[1])
    return temp


def catch_exception(func):
    def catcher(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            common_log.error(e)
            return 'Что-то пошло не так, сообщите об это моему создателю!'
    return catcher


class QuoteTelegramBotView(CSRFExemptInMixin, LogViewMixin, View):

    def __init__(self, **kwargs):
        super(QuoteTelegramBotView, self).__init__(**kwargs)
        self.commands = {
            '/start': self._display_help,
            'help': self._display_help,
            '/help': self._display_help,
            'muse': self._get_random_quote,
            '/muse': self._get_random_quote,
            'category': self._get_random_quote_by_category,
            '/category': self._get_random_quote_by_category
        }

    def get_log_name(self):
        return 'telegram_quote_bot_log'

    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid bot token!')

        try:
            user_message = json.loads(request.body.decode('utf-8'), 'utf-8')
        except ValueError:
            return HttpResponseBadRequest('Invalid request body!')

        chat_id = user_message['message']['chat']['id']
        cmd = user_message['message'].get('text')

        if cmd:
            user_command = cmd.split()
            func = self._get_command(user_command[0])
            params = user_command[1:]
            QuoteTelegramBot.sendMessage(chat_id, func(params), parse_mode='Markdown')

        return JsonResponse({}, status=200)

    def _get_command(self, raw_cmd):
        what = raw_cmd.split('@')[0].lower()
        func = self.commands.get(what) or self.commands.get('help')
        return func

    @catch_exception
    def _get_random_quote(self, args=()):
        self.log_info('Запрошена случайная цитата')
        return Quote.quote_manager.get_random_quotes(1)[0].build_quote()

    @catch_exception
    @filter_category
    def _get_random_quote_by_category(self, category):
        quotes = Quote.quote_manager.get_random_quotes_by_category(category, 1)
        self.log_info('Запрошена случайная цитата по категории %s' % category.name)
        return quotes[0].build_quote()

    @catch_exception
    def _display_help(self, args=()):
        self.log_info('Запрошена помощь бота')
        return render_to_string('quotes/telegram_bot_help.md')
