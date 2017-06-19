# -*- coding: utf-8 -*-

from nemodev_platform import settings


# Отформатировать дату
def format_date(value, arg=''):
    return value.strftime(arg if arg else settings.DATE_FORMAT)
