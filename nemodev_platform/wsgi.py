import os
import sys

from django.core.wsgi import get_wsgi_application

path = '/home/base'
if path not in sys.path:
    sys.path.append(path)

from nemodev_platform.settings_helper import *
os.environ['DJANGO_SETTINGS_MODULE'] = SETTINGS_MODULE

if PRODUCTION:
    from whitenoise.django import DjangoWhiteNoise
    application = DjangoWhiteNoise(get_wsgi_application())
else:
    application = get_wsgi_application()
