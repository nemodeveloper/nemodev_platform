# coding=utf-8
from django.db import models

# Create your models here.
from src.apps.ext_user.models import ExtUser
from src.core.utils.datetime import current_date


class WorkTime(models.Model):

    user = models.ForeignKey(to=ExtUser, verbose_name=u'Пользователь', related_name='work_times',
                             on_delete=models.CASCADE)
    start_time = models.DateTimeField(u'Начало работы', default=current_date(), null=False, db_index=True)
    end_time = models.DateTimeField(u'Конец работы', null=True, db_index=True)

    def __str__(self):
        return ''

    class Meta:
        verbose_name = u'Рабочее время'
        verbose_name_plural = u'Рабочее время'
        db_table = 'work_time'
        default_permissions = ()
        permissions = (
            ('add_work_time', 'Добавление рабочего времени'),
            ('change_work_time', 'Обновление рабочего времени'),
            ('delete_work_time', 'Удаление рабочего времени'),
        )
