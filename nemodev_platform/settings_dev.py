# -*- coding: utf-8 -*-
from .settings import *

LOGGING['loggers']['django.db.backends'] = {
            'level': 'DEBUG',
            'handlers': ['console_sql'],
            'propagate': False,
}

