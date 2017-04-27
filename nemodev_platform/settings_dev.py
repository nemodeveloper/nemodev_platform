# -*- coding: utf-8 -*-
from .settings import LOGGING

DATABASE_NAME = 'dev_muse_db'
DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.%s' % DATABASE_ENGINE,
        'NAME': DATABASE_NAME,
        'USER': 'dev_muse',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'CONN_MAX_AGE': 60,
    }
}

LOGGING['loggers']['django.db.backends'] = {
            'level': 'DEBUG',
            'handlers': ['console_sql'],
            'propagate': False,
}
