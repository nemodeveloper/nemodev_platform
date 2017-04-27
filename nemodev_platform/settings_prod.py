# -*- coding: utf-8 -*-

# from .settings import *


DATABASE_NAME = 'muse_db'
DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.%s' % DATABASE_ENGINE,
        'NAME': DATABASE_NAME,
        'USER': 'muse',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',
        'PORT': '',
        'CONN_MAX_AGE': 60,
    }
}

