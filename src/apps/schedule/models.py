from django.db import models

# Create your models here.

from nemodev_platform import settings
from src.utils.common.datetime import format_date


# Учебная четверть
class SchoolQuarter(models.Model):

    QUARTER_NUMBER_CHOICES = (
        ('1', 'Первая'),
        ('2', 'Вторая'),
        ('3', 'Третья'),
        ('4', 'Четвертая'),
    )

    quarter_number = models.CharField(u'Учебная четверть', choices=QUARTER_NUMBER_CHOICES, max_length=1)
    start_date = models.DateField(u'Начало учебной четверти')
    end_date = models.DateField(u'Конец учебной четверти')

    def __str__(self):
        return '%s учебная четверть c %s по %s' % (
            self.get_quarter_number_display(),
            format_date(self.start_date, settings.SHORT_DATE_FORMAT),
            format_date(self.end_date, settings.SHORT_DATE_FORMAT))

    class Meta:
        verbose_name = u"Учебная четверть"
        verbose_name_plural = u"Учебные четверти"
        db_table = u'schedule_school_quarter'
        permissions = (
            ('add_school_quarter_entity', 'Добавление учебной четверти'),
            ('update_school_quarter_entity', 'Редактирование учебной четверти'),
            ('delete_school_quarter_entity', 'Удаление учебной четверти'),
        )


# Учебная план по предметам
class WorkPlan(models.Model):

    SUBJECT_WEEK_PERIOD_CHOICES = (
        ('EVERY_WEEK', u'Каждая неделя'),
        ('EVEN_WEEK', u'Первая неделя'),
        ('ODD_WEEK', u'Вторая неделя'),
    )

    school_quarter = models.ForeignKey(to='SchoolQuarter', verbose_name='Четверть', related_name='work_plan',
                                       on_delete=models.PROTECT)
    school_class = models.ForeignKey(to='catalogs.SchoolClass', verbose_name=u'Класс', related_name='work_plan',
                                     on_delete=models.PROTECT)
    sub_class = models.ForeignKey(to='catalogs.SchoolClassGroup', verbose_name='Подгруппа', on_delete=models.PROTECT)
    subject = models.ForeignKey(to='catalogs.Subject', verbose_name='Учебный предмет', related_name='work_plan',
                                on_delete=models.PROTECT)
    subject_period = models.CharField(u'Учебная неделя', choices=SUBJECT_WEEK_PERIOD_CHOICES, max_length=10)
    week_lesson_count = models.IntegerField(u'Уроков в неделю')
    total_lesson_count = models.IntegerField(u'Всего уроков')

    def __str__(self):
        return 'Учебный план'

    class Meta:
        verbose_name = u"Учебный план"
        verbose_name_plural = u"Учебные планы"
        db_table = u'schedule_work_plan'
        permissions = (
            ('add_work_plan_entity', 'Добавление учебного плана'),
            ('update_work_plan_entity', 'Редактирование учебного плана'),
            ('delete_work_plan_entity', 'Удаление учебного плана'),
        )


# Расписание звонков
class LessonTime(models.Model):

    begin_time = models.TimeField(u'Время начала урока')
    end_time = models.TimeField(u'Время окончания урока')
    rest_time = models.TimeField(u'Перерыв после урока')

    def __str__(self):
        return '%s - %s' % (format_date(self.begin_time, '%H:%M'), format_date(self.end_time, '%H:%M'))

    class Meta:
        ordering = ('begin_time',)
        verbose_name = u"Расписание звонков"
        verbose_name_plural = u"Расписание звонков"
        db_table = u'catalogs_lesson_time'
        default_permissions = ()
        permissions = (
            ('add_lesson_time_entity', 'Добавление расписания звонков'),
            ('update_lesson_time_entity', 'Редактирование расписания звонков'),
            ('delete_lesson_time_entity', 'Удаление расписания звонков'),
        )


# Учебное расписание
class Lesson(models.Model):

    LESSON_DAYS = {
        1: u'Понедельник',
        2: u'Вторник',
        3: u'Среда',
        4: u'Четверг',
        5: u'Пятница',
        6: u'Суббота'
    }

    STATUS_CHOICES = (
        ('DONE', u'Урок проведен'),
        ('CANCELED', u'Урок отменен'),
        ('MOVED', u'Урок перенесен'),
    )

    lesson_date = models.DateTimeField(u'Время урока')
    school_class = models.ForeignKey(to='catalogs.SchoolClass', verbose_name=u'Класс', on_delete=models.PROTECT)
    subject = models.ForeignKey(to='catalogs.Subject', verbose_name=u'Предмет', on_delete=models.PROTECT)
    classroom = models.ForeignKey(to='catalogs.ClassRoom', verbose_name=u'Кабинет', on_delete=models.PROTECT)
    teacher = models.ForeignKey(to='catalogs.Teacher', verbose_name=u"Учитель", on_delete=models.PROTECT)
    lesson_status = models.CharField(u'Статус урока', choices=STATUS_CHOICES, max_length=8, default='DONE')
    description = models.CharField(u'Доп.информация', max_length=100, null=True, blank=True)

    def __str__(self):
        return 'Урок'

    class Meta:
        verbose_name = u'Расписание уроков'
        verbose_name_plural = u'Расписание уроков'
        db_table = u'schedule_lessons'
        permissions = (
            ('add_schedule_entity', 'Добавление уроков'),
            ('edit_schedule_entity', 'Редактирование уроков'),
            ('delete_schedule_entity', 'Удаление уроков'),
        )
