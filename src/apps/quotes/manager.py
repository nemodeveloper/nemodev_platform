# -*- coding: utf-8 -*-
from django.db import models


class QuoteManager(models.Manager):

    # Получить случайный набор цитат
    def get_random_quotes(self, count):
        result = super(QuoteManager, self).get_queryset().order_by('?')[:count]

        # raw(
        #     "SELECT DISTINCT * FROM %s LIMIT %d OFFSET ABS(RANDOM()) % (SELECT COUNT(*) FROM %s)",
        #     params=[table, count, table]
        # )
        return result
