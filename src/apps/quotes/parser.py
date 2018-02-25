# -*- coding: utf-8 -*-
import json
import os

from django.db import transaction

from src.apps.quotes.models import Category, Author, Quote


class QuoteParser(object):

    def __init__(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError('File %s not exists!' % file_path)

        self.file_path = file_path
        self.raw_data = []
        self.quote_list = []

        self.authors_cache = {}
        self.categories_cache = {}

    def process(self):
        self._parse()
        self._process_raw_data()
        self._show_statistic()

    def _parse(self):
        print('Начинаем парсинг файла %s ...' % self.file_path)
        with open(self.file_path, encoding='utf-8') as quote_file:
            self.raw_data = json.load(quote_file)
        print('Завершили парсинг файла %s !' % self.file_path)

    @transaction.atomic()
    def _process_raw_data(self):
        print('Начинаем обработку сырых данных...')

        for raw_category in self.raw_data:
            category = self._get_or_create_category(raw_category['name'].capitalize())
            for raw_quote in raw_category['quotes']:
                quote = self._create_quote(category, raw_quote)
                if quote:
                    self.quote_list.append(quote)

        Quote.objects.bulk_create(self.quote_list)
        print('Завершили обработку сырых данных!')

    def _show_statistic(self):
        print('Всего авторов - %s' % len(self.authors_cache))
        print('Всего категорий - %s' % len(self.categories_cache))
        print('Всего цитат - %s' % len(self.quote_list))

    def _get_or_create_category(self, category_name):
        category = self.categories_cache.get(category_name)
        if not category:
            category = Category.objects.create(name=category_name)
            self.categories_cache[category_name] = category
        return category

    def _create_quote(self, category, raw_quote):

            raw_text = raw_quote['text'].\
                replace('&nbsp;', ' ').\
                replace('<br>', '').strip()

            if not raw_text:
                return None

            raw_author = raw_quote['author']
            author = None
            if raw_author:
                author = self._get_or_create_author(raw_author)

            raw_source = raw_quote['source']
            if raw_source:
                raw_source = raw_source.replace('&nbsp;', ' ').strip()

            raw_year = raw_quote['year'].replace('&nbsp;', ' ').strip() \
                if raw_quote['year'] else None

            quote = Quote(
                category=category,
                text=raw_text,
                author=author,
                source=raw_source,
                year=raw_year
            )

            return quote

    def _get_or_create_author(self, author_name):
        author_name = author_name.strip()
        author = self.authors_cache.get(author_name)
        if not author:
            author = Author.objects.create(full_name=author_name)
            self.authors_cache[author_name] = author
        return author
