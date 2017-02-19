# -*- coding: utf-8 -*-
import logging

import telepot
from django.template.loader import render_to_string
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, \
    InputTextMessageContent

from nemodev_platform import settings

from src.apps.quotes.models import Quote, Category, Author
from src.base.view.log import LogMixin

QuoteTelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)
QuoteTelegramBot.setWebhook('https://quotesformuse.ru/quotes/bot/%s/' % settings.TELEGRAM_BOT_TOKEN)


common_log = logging.getLogger('common_log')


def filter_category(func):
    def temp(*args, **kwargs):
        if args[1]:
            raw_category = args[1][0].lower().title()
            category = Category.objects.filter(name__startswith=raw_category).first()
            if category:
                return func(args[0], category)
        return 'К сожалению мне не удалось ничего найти по запросу %s' % ' '.join(args[1])
    return temp


def filter_author(func):
    def temp(*args, **kwargs):
        if args[1]:
            raw_author = args[1][0].lower().title()
            author = Author.objects.filter(full_name__contains=raw_author).first()
            if author:
                return func(args[0], author)
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


def render_quote(func):
    def temp(*args, **kwargs):
        return func(args[0], args[1]).build_quote()
    return temp


class BaseMessageProcessor(LogMixin):

    def __init__(self, user_message):
        super(BaseMessageProcessor, self).__init__()
        self.user_message = user_message
        self.commands = self._get_commands()

    def get_log_name(self):
        return 'telegram_quote_bot_log'

    def _get_commands(self):
        return {
            '/start': self._display_help,
            '/commands': self._display_commands,
            'help': self._display_help,
            '/help': self._display_help,
            'q': self._get_random_quote,
            '/q': self._get_random_quote,
            'c': self._get_random_quote_by_category,
            '/c': self._get_random_quote_by_category,
            'a': self._get_random_quote_by_author,
            '/a': self._get_random_quote_by_author
        }

    def get_chat_id(self):
        raise NotImplementedError('Realise me!')

    def process(self):
        raise NotImplementedError('Realise me!')

    def send_message(self, text):
        QuoteTelegramBot.sendMessage(self.get_chat_id(), text, parse_mode='Markdown')

    def send_inline_message(self, results):
        QuoteTelegramBot.answerInlineQuery(self.get_chat_id(), results)

    @catch_exception
    @render_quote
    def _get_random_quote(self, args=()):
        self.log_info('Запрошена случайная цитата')
        return Quote.quote_manager.get_random_quotes(1)[0]

    @catch_exception
    @filter_category
    @render_quote
    def _get_random_quote_by_category(self, category):
        quotes = Quote.quote_manager.get_random_quotes_by_category(category, 1)
        self.log_info('Запрошена случайная цитата по категории %s' % category.name)
        return quotes[0]

    @catch_exception
    @filter_author
    @render_quote
    def _get_random_quote_by_author(self, author):
        quotes = Quote.quote_manager.get_random_quotes_by_author(author, 1)
        self.log_info('Запрошена случайная цитата по автору %s' % author.full_name)
        return quotes[0]

    @catch_exception
    def _display_help(self, args=()):
        return render_to_string('quotes/telegram_bot_help.md')

    @catch_exception
    def _display_commands(self, args=()):
        return render_to_string('quotes/telegram_bot_commands.md')


# Класс обрабатывает простую команду пользователя телеграм типа - message
class SimpleMessageProcessor(BaseMessageProcessor):

    def __init__(self, user_message):
        super(SimpleMessageProcessor, self).__init__(user_message)
        self.message = self.user_message['message']
        self.cmd = self.message.get('text')

    # получить обработчик команды клиента
    def _get_command(self, raw_cmd):
        what = raw_cmd.split('@')[0].lower()
        func = self.commands.get(what) or self.commands.get('help')
        return func

    def get_chat_id(self):
        return self.message['chat']['id']

    def process(self):
        if self.cmd:
            user_command = self.cmd.split()
            self.log_info('SimpleMessageProcessor запрос пользователя - %s' % user_command)
            func = self._get_command(user_command[0])
            params = user_command[1:]
            self.send_message(func(params))


class InlineMessageProcessor(BaseMessageProcessor):

    def __init__(self, user_message):
        super(InlineMessageProcessor, self).__init__(user_message)
        self.inline_message = self.user_message['inline_query']
        self.query = self.inline_message.get('query')
        self.query = self.query.strip() if self.query else ''

    def _get_commands(self):
        return {
            'c': self._get_categories,
            '/c': self._get_categories,
            'a': self._get_authors,
            '/a': self._get_authors,
        }

    def _get_categories(self):
        categories = Category.category_manager.get_random_category(5)
        result = []
        for category in categories:
            result.append(InlineQueryResultArticle(
                id="c|%s" % category.id, title=category.name,
                input_message_content=InputTextMessageContent(message_text=category.name, parse_mode='Markdown'))
            )

        return result

    def _get_authors(self):
        authors = Author.author_manager.get_random_author(5)
        result = []
        for author in authors:
            result.append(InlineQueryResultArticle(
                id="a|%s" % author.id, title=author.full_name,
                input_message_content=InputTextMessageContent(message_text=author.full_name, parse_mode='Markdown'))
            )

        return result

    def process(self):
        command = self.commands.get(self.query)
        if command:
            self.send_inline_message(command())

    def get_chat_id(self):
        return self.inline_message['id']


# Маршрутизация запросов
router = {
    'message': SimpleMessageProcessor,
    'inline_query': InlineMessageProcessor,
}


# Получить процессор сообщения исходя из типа запроса клиента
def get_processor(user_message):
    mess_type = None
    if user_message.get('message'):
        mess_type = 'message'
    elif user_message.get('inline_query'):
        mess_type = 'inline_query'

    processor = router.get(mess_type)

    return processor(user_message) if processor else processor
