import telepot

from nemodev_platform import settings

QuoteTelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)
QuoteTelegramBot.setWebhook('https://quotesformuse.ru/quotes/bot/%s/' % settings.TELEGRAM_BOT_TOKEN)
