# -*- coding: utf-8 -*-
import os

from django.core.management import BaseCommand

from nemodev_platform.settings import BASE_DIR
from src.apps.quotes.parser import QuoteParser

BASE_QUOTES_FILE = 'database/GreatWordsQuotes.json'


# Загрузчик базы данных цитат
class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Инициирована загрузка цитат в базу данных...')

        file = os.path.join(BASE_DIR, BASE_QUOTES_FILE)
        if os.path.exists(file):
            quote_parser = QuoteParser(file)
            quote_parser.process()
        else:
            print('Файл %s не найден...' % file)

        print('Загрузка цитат в базу данных завершена...')
