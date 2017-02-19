# -*- coding: utf-8 -*-
from django.db import models


class QuoteManager(models.Manager):

    # Получить случайный набор цитат
    def get_random_quotes(self, count):
        # raw(
        #     "SELECT DISTINCT * FROM %s LIMIT %d OFFSET ABS(RANDOM()) % (SELECT COUNT(*) FROM %s)",
        #     params=[table, count, table]
        # )
        return super(QuoteManager, self).get_queryset().select_related('category', 'author').order_by('?')[:count]

    def get_random_quotes_with_author(self, count):
        return super(QuoteManager, self).get_queryset().select_related('category', 'author').exclude(author__isnull=True).order_by('?')[:count]

    # Получить случайный набор цитат по категории
    def get_random_quotes_by_category(self, category, count):
        if category:
            result = super(QuoteManager, self).get_queryset().select_related('category', 'author').filter(category=category).order_by('?')[:count]
        else:
            result = []

        return result

    # Получить случайный набор цитат по автору
    def get_random_quotes_by_author(self, author, count):
        if author:
            result = super(QuoteManager, self).get_queryset().select_related('category', 'author').filter(
                author=author).order_by('?')[:count]
        else:
            result = []

        return result


class CategoryManager(models.Manager):

    def get_random_category(self, count):
        return super(CategoryManager, self).get_queryset().order_by('?')[:count]


class AuthorManager(models.Manager):

    def get_random_author(self, count):
        return super(AuthorManager, self).get_queryset().order_by('?')[:count]
