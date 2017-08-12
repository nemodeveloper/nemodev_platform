# -*- coding: utf-8 -*-
from django.utils import timezone

from nemodev_platform import settings


# Отформатировать дату
def format_date(date, date_format):
    return date.strftime(date_format if date_format else settings.DATE_FORMAT)


# Получить текущую дату
def current_date():
    return timezone.now()
