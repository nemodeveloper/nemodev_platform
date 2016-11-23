from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Некоректное поле Email')

        user = self.model(email=UserManager.normalize_email(email),)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class ExtUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('Электронная почта'), max_length=255, unique=True, db_index=True)
    register_date = models.DateField(_('Дата регистрации'), default=timezone.now())
    is_active = models.BooleanField(_('Активен'), default=True)
    is_admin = models.BooleanField(_('Администратор'), default=False)

    def get_full_name(self):
        return self.get_short_name()

    def get_short_name(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.get_full_name()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        db_table = 'ext_user_user'
        default_permissions = ()
        permissions = (
            ('add_ext_user', 'Добавление пользователей'),
            ('change_ext_user', 'Обновление информации пользователя'),
            ('delete_ext_user', 'Удаление пользователя'),
        )
