# -*- coding: utf-8 -*-
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# Базовый класс проверки пользователя на наличие входа в систему
class LoggedMixin:

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoggedMixin, self).dispatch(request, *args, **kwargs)


# Базовый класс для доступа к функционалу административной части
class AdminMixin:

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AdminMixin, self).dispatch(request, *args, **kwargs)


# Базовый класс для работы с системы, без csrf - токена
class CSRFExemptMixin:

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(request, *args, **kwargs)


# Примесь предоставляет утилитный метод для проверки прав клиента
class UserPermMixin:

    # Проверить у пользователя наличие права на работу с ситемой
    def check_perm(self, user, perm_key):
        have_perm = False
        if user and user.is_authenticated:
            if user.is_superuser:
                have_perm = True
            else:
                have_perm = user.has_perm(perm_key)
        return have_perm

