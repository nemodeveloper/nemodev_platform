import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django_jinja.builtins import DEFAULT_EXTENSIONS

from nemodev_platform.secret_key_generator import generator

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Start project definition

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = generator.get_app_secret_key(BASE_DIR)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
ROOT_URLCONF = 'nemodev_platform.urls'
WSGI_APPLICATION = 'nemodev_platform.wsgi.application'

# End project definition

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

EXTERNAL_APPS = [
    'django_jinja2',
]

PROJECT_APPS = [
    'src.apps.ext_user.apps.ExtUserConfig',
    'src.apps.quotes.apps.QuotesConfig'
]

INSTALLED_APPS += EXTERNAL_APPS + PROJECT_APPS

# Start middleware definition

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 24 * 60 * 60       # куки живут 24 часа

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'src.core.middleware.request.RequestMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# End middleware definition

# Start templates definition

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates/jinja2/'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'nemodev_platform.jinja2.environment',
            'extensions': DEFAULT_EXTENSIONS,
            'auto_reload': DEBUG,
            'autoescape': True,
        },
    },
]

# End templates definition

# Start database definition
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASE_NAME = 'dev_db.sqlite3'
DATABASE_ENGINE = 'sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.%s' % DATABASE_ENGINE,
        'NAME': os.path.join(BASE_DIR, 'database/%s' % DATABASE_NAME),
    }
}

# End database definition

# Start internationalization definition
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = False
USE_TZ = False

DATE_TIME_FORMAT_WITH_SEC = '%d.%m.%Y %H:%M:%S'
DATE_TIME_FORMAT = '%d.%m.%Y %H:%M'
DATE_FORMAT = '%d.%m.%Y'

# End internationalization definition

# Start logs definitions

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },

    'formatters': {
        'verbose': {
            'format': u'[%(levelname)s] [%(asctime)s] [%(module)s] [%(process)d] [%(thread)d] [%(message)s]',
            'datefmt': DATE_TIME_FORMAT_WITH_SEC,
        },
        'simple': {
            'format': u'[%(levelname)s] [%(message)s]'
        },
        'sql': {
            'format': u'[%(levelname)s] [%(asctime)s]\n[sql_duration=%(duration)s]\n[sql_text=%(sql)s]\n[sql_params=%(params)s]',
            'datefmt': DATE_TIME_FORMAT_WITH_SEC,
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'console_sql': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'sql',
            'filters': ['require_debug_true'],
        },
        'common_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 5,
            'encoding': 'utf-8',
            'filename': os.path.join(BASE_DIR, 'logs/common.log'),
            'formatter': 'verbose',
            'filters': [],
        },
        'telegram_quote_bot_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 10 * 1024 * 1024,
            'encoding': 'utf-8',
            'filename': os.path.join(BASE_DIR, 'logs/telegram_quote_bot.log'),
            'formatter': 'verbose',
            'filters': [],
        },
    },

    'loggers': {
        'common_log': {
            'handlers': ['common_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'telegram_quote_bot_log': {
            'handlers': ['telegram_quote_bot_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'level': 'WARNING',
            'handlers': ['common_file', 'console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['common_file', 'console'],
            'level': 'WARNING',
            'propagate': True,
        },
        '': {
            'level': 'WARNING',
            'handlers': ['common_file', 'console'],
            'propagate': True,
        }
    }
}

# End logs definitions

# Start static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static_dir', 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'static_dir', 'media')
MEDIA_URL = '/media/'

# место для статики
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'templates/src/'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# upload files config
FILE_UPLOAD_TEMP_DIR = os.path.join(BASE_DIR, 'temp')
FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler"
]

# End static files (CSS, JavaScript, Images)

# Start CSA definition

LOGIN_URL = '/csa/login/'
LOGOUT_URL = '/csa/logout/'
AUTH_USER_MODEL = 'ext_user.ExtUser'

# End CSA definition

# Start tastypie config

TASTYPIE_ALLOW_MISSING_SLASH = True
TASTYPIE_DEFAULT_FORMATS = ['json']

# End tastypie config

# Start telegram bot config
TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN', 'test')
# End telegram bot config

if DEBUG:
    from .settings_dev import *
else:
    from .settings_prod import *
