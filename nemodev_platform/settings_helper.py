import socket

from nemodev_platform.settings_prod import ALLOWED_HOSTS

PRODUCTION = True if socket.gethostname() in ALLOWED_HOSTS else False
SETTINGS_MODULE = 'nemodev_platform.settings_prod' if PRODUCTION else 'nemode_platform.settings_dev'