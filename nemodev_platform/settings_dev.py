# -*- coding: utf-8 -*-
from nemodev_platform.settings import *


SHOW_SQL_IN_CONSOLE = env.bool('SHOW_SQL', False)

DEBUG_APPS = [
    'debug_toolbar'
]

INSTALLED_APPS += DEBUG_APPS

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

DATABASES = {
    'default': env.db(),
}

if SHOW_SQL_IN_CONSOLE:
    LOGGING['loggers']['django.db.backends'] = {
                'level': 'DEBUG',
                'handlers': ['console_sql'],
                'propagate': False,
    }

TEMPLATES += [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Start debug-toolbar definition

INTERNAL_IPS = ['127.0.0.1']
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

# End debug-toolbar definition
