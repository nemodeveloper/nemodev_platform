import socket

from nemodev_platform.settings_prod import ALLOWED_HOSTS

PRODUCTION = socket.gethostname() in ALLOWED_HOSTS
SETTINGS_MODULE = 'nemodev_platform.settings_prod' if PRODUCTION else 'nemodev_platform.settings_dev'