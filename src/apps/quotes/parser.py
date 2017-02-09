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

    def process(self):
        self._parse()
        self._process_raw_data()

    def _parse(self):
        print('Начинаем парсинг файла %s ...' % self.file_path)
        with open(self.file_path, encoding='utf-8') as quote_file:
            self.raw_data = json.load(quote_file)
        print('Завершили парсинг файла %s !' % self.file_path)

    def _process_raw_data(self):
        print('Начинаем обработку сырых данных...')

        for raw_category in self.raw_data:
            category = self._get_or_create_category(raw_category['name'].capitalize())
            for raw_quote in raw_category['quotes']:
                quote = QuoteParser._create_quote(category, raw_quote)
                if quote:
                    self.quote_list.append(quote)

        Quote.objects.bulk_create(self.quote_list)
        print('Завершили обработку сырых данных!')

    @staticmethod
    def _get_or_create_category(category_name):
        category = Category.objects.filter(name=category_name).first()
        if not category:
            category = Category.objects.create(name=category_name)
        return category

    @staticmethod
    def _create_quote(category, raw_quote):

        with transaction.atomic():
            raw_text = raw_quote['text'].\
                replace('&nbsp;', ' ').\
                replace('<br>', '').strip()

            if not raw_text:
                return None

            raw_author = raw_quote['author']
            author = None
            if raw_author:
                author = QuoteParser._get_or_create_author(raw_author)

            raw_source = raw_quote['source']
            if raw_source:
                raw_source = raw_source.replace('&nbsp;', ' ')

            raw_year = raw_quote['year']

            quote = Quote(
                category=category,
                text=raw_text,
                author=author,
                source=raw_source,
                year=raw_year
            )

            return quote

    @staticmethod
    def _get_or_create_author(author_name):
        author = Author.objects.filter(full_name=author_name).first()
        if not author:
            author = Author.objects.create(full_name=author_name)
        return author
