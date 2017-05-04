# -*- coding: utf-8 -*-
import logging

import telepot
from django.template.loader import render_to_string
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, \
    InputTextMessageContent, ReplyKeyboardMarkup, KeyboardButton

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
        if len(args) > 1:
            return func(args[0], args[1]).build_quote()
        else:
            return func(args[0]).build_quote()
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
            'start': self._display_help,
            'help': self._display_help,
        }

    def get_chat_id(self):
        raise NotImplementedError('Realise me!')

    def process(self):
        raise NotImplementedError('Realise me!')

    def send_text_message(self, text):
        QuoteTelegramBot.sendMessage(self.get_chat_id(), text, parse_mode='Markdown')

    def send_markup_message(self, text, markup):
        QuoteTelegramBot.sendMessage(chat_id=self.get_chat_id(), text=text, reply_markup=markup)

    def send_inline_message(self, results):
        QuoteTelegramBot.answerInlineQuery(self.get_chat_id(), results, cache_time=0)

    @catch_exception
    @render_quote
    def _get_random_quote(self):
        self.log_info('Запрошена случайная цитата')
        return Quote.quote_manager.get_random_quotes(1)[0]

    @catch_exception
    @filter_category
    @render_quote
    def _get_random_quote_by_category(self, category):
        self.log_info('Запрошена случайная цитата по категории %s' % category.name)
        return Quote.quote_manager.get_random_quotes_by_category(category, 1)[0]

    @catch_exception
    @filter_author
    @render_quote
    def _get_random_quote_by_author(self, author):
        self.log_info('Запрошена случайная цитата по автору %s' % author.full_name)
        return Quote.quote_manager.get_random_quotes_by_author(author, 1)[0]

    @catch_exception
    def _display_help(self):
        return render_to_string('quotes/telegram_bot_help.md')


# Класс обрабатывает простую команду пользователя телеграм типа - text
class TextMessageProcessor(BaseMessageProcessor):

    def __init__(self, user_message):
        super(TextMessageProcessor, self).__init__(user_message)
        self.message = self.user_message['message']
        self.cmd = self.message.get('text').strip('/')

    def _get_commands(self):
        base_commands = super(TextMessageProcessor, self)._get_commands()
        base_commands['q'] = self._get_random_quote

        return base_commands

    # получить обработчик команды клиента
    def _get_command(self, cmd):
        return self.commands.get(cmd)

    def get_chat_id(self):
        return self.message['chat']['id']

    def process(self):
        if self.cmd:
            self.log_info('TextMessageProcessor запрос пользователя - %s' % self.cmd)
            func = self._get_command(self.cmd)
            if func:
                self.send_text_message(func())


class InlineMessageProcessor(BaseMessageProcessor):

    def __init__(self, user_message):
        super(InlineMessageProcessor, self).__init__(user_message)
        self.inline_message = self.user_message['inline_query']
        self.query = self.inline_message.get('query')
        self.query = self.query.strip().strip('/') if self.query else ''

    def _get_commands(self):
        return {
            '': self._show_quote_choice,
            'c': self._get_categories,
            'a': self._get_authors,
        }

    def _get_categories(self):
        quotes = Quote.quote_manager.get_random_quotes(5)
        result = []
        for quote in quotes:
            result.append(InlineQueryResultArticle(
                id="c|%s" % quote.category.id, title=quote.category.name,
                input_message_content=InputTextMessageContent(
                    message_text=quote.build_quote(), parse_mode='Markdown'))
            )

        return result

    def _get_authors(self):
        quotes = Quote.quote_manager.get_random_quotes_with_author(5)
        result = []
        for quote in quotes:
            result.append(InlineQueryResultArticle(
                id="a|%s" % quote.author.id, title=quote.author.full_name,
                input_message_content=InputTextMessageContent(
                    message_text=quote.build_quote(), parse_mode='Markdown'))
            )

        return result

    def _show_quote_choice(self):
        keyboards = [
            ['Случайная'],
            ['По категории', 'По автору'],
        ]

        markup = ReplyKeyboardMarkup(
            keyboard=keyboards,
            resize_keyboard=True,
            one_time_keyboard=True
        )

        return 'Выберите тип цитаты', markup

    def process(self):
        command = self.commands.get(self.query)
        if command:
            result = command()
            if self.query == '':
                return self.send_markup_message(result[0], result[1])
            return self.send_inline_message(result)

    def get_chat_id(self):
        return self.inline_message['id']


# Маршрутизация запросов
router = {
    'message': TextMessageProcessor,
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
