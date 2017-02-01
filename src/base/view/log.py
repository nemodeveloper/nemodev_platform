# -*- coding: utf-8 -*-

import logging


# Примись для логирования в конкретный LOG из settings.LOGGING
class LogViewMixin(object):

    def __init__(self):
        super(LogViewMixin, self).__init__()
        self.logger = logging.getLogger(self.get_log_name())

    # Получить имя лога
    def get_log_name(self):
        raise NotImplementedError('Implement method - get_log_name!')

    def log_debug(self, message=''):
        try:
            self.logger.debug(msg=message)
        except Exception as e:
            print(e)

    def log_info(self, message=''):
        try:
            self.logger.info(msg=message)
        except Exception as e:
            print(e)

    def log_warning(self, message=''):
        try:
            self.logger.warning(msg=message)
        except Exception as e:
            print(e)

    def log_error(self, message=''):
        try:
            self.logger.error(msg=message)
        except Exception as e:
            print(e)
