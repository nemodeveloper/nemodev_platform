import os
import sys

from django.core.wsgi import get_wsgi_application

path = '/home/base'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'nemodev_platform.settings'

from nemodev_platform.settings import DEBUG

if not DEBUG:
    from whitenoise.django import DjangoWhiteNoise
    application = DjangoWhiteNoise(get_wsgi_application())
else:
    application = get_wsgi_application()
