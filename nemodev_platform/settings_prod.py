# -*- coding: utf-8 -*-
from nemodev_platform.settings import *

DATABASES = {
    'default': env.db(),
}
