# -*- coding: utf-8 -*-


from django.conf.urls import url

from src.apps.quotes.views import QuoteTelegramBotView

urlpatterns = [
    url(r'^bot/(?P<bot_token>.+)/$', QuoteTelegramBotView.as_view(), name='quote_telegram_bot'),
]
