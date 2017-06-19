# -*- coding: utf-8 -*-
from nemodev_platform.settings import env

DATABASES = {
    'default': env.db(),
}
