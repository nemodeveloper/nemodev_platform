from django.db import models

# Create your models here.


# Учебный кабинет
from src.utils.common.datetime import format_date


class ClassRoom(models.Model):

    room_name = models.CharField(u'Название учебного кабинета', max_length=20, unique=True)

    def __str__(self):
        return self.room_name

    class Meta:
        verbose_name = u'Учебный кабинет'
        verbose_name_plural = u'Учебные кабинеты'
        db_table = 'catalogs_class_rooms'
        default_permissions = ()
        permissions = (
            ('add_class_room', 'Добавление учебного кабинета'),
            ('update_class_room', 'Редактирование учебного кабинета'),
            ('delete_class_room', 'Удаление учебного кабинета'),
        )


# Учебный предмет
class Subject(models.Model):

    SUBJECT_TYPE_CHOICES = (
        ('COMMON', u'Общий'),
        ('TECH', u'Технический'),
        ('HUMANIT', u'Гуманитарный'),
    )

    sub_name = models.CharField(u'Название предмета', max_length=25, unique=True)
    sub_short_name = models.CharField(u'Краткое название предмета', max_length=12)
    weight = models.IntegerField(u'Вес предмета')
    subject_type = models.CharField(u'Тип предмета', choices=SUBJECT_TYPE_CHOICES, max_length=7)
    class_rooms = models.ManyToManyField(
        to='ClassRoom', verbose_name=u'Учебные кабинеты', related_name='subjects')

    def __str__(self):
        return self.sub_name

    class Meta:
        verbose_name = 'Учебный предмет'
        verbose_name_plural = 'Учебные предметы'
        db_table = 'catalogs_subjects'
        default_permissions = ()
        permissions = (
            ('add_subject_entity', 'Добавление учебного предмета'),
            ('update_subject_entity', 'Редактирование учебного предмета'),
            ('delete_subject_entity', 'Удаление учебного предмета'),
        )


# Учебный класс
class SchoolClass(models.Model):

    class_name = models.CharField('Учебный класс', max_length=15, unique=True)

    def __str__(self):
        return self.class_name

    class Meta:
        verbose_name = 'Учебный класс'
        verbose_name_plural = 'Учебные классы'
        db_table = 'catalogs_school_class'
        default_permissions = ()
        permissions = (
            ('add_school_class_entity', 'Добавление учебного класса'),
            ('update_school_class_entity', 'Редактирование учебного класса'),
            ('delete_school_class_entity', 'Удаление учебного класса'),
        )


# Деление учебных классов на подгруппы по предметам
class SchoolClassGroup(models.Model):

    school_class = models.ForeignKey(to='SchoolClass', verbose_name=u'Учебный класс', related_name='school_class_group',
                                     on_delete=models.PROTECT)
    subject = models.ForeignKey(to='Subject', verbose_name=u'Учебный предмет', on_delete=models.PROTECT)
    group_name = models.CharField(u'Название подгруппы', max_length=20)

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = 'Подгруппы по классам'
        verbose_name_plural = 'Подгруппы по классам'
        db_table = 'catalogs_school_class_group'
        default_permissions = ()
        permissions = (
            ('add_school_class_group_entity', 'Добавление подгруппы класса'),
            ('update_school_class_group_entity', 'Редактирование подгруппы класса'),
            ('delete_school_class_group_entity', 'Удаление подгруппы класса'),
        )


# Преподаватель
class Teacher(models.Model):

    last_name = models.CharField(u'Фамилия', max_length=20)
    first_name = models.CharField(u'Имя', max_length=15)
    father_name = models.CharField(u'Отчество', max_length=15)
    subjects = models.ManyToManyField(to='Subject', verbose_name=u'Предметы', related_name=u'teachers')

    def __str__(self):
        return "%s %s %s" % (self.last_name, self.first_name, self.father_name)

    class Meta:
        verbose_name = u'Учитель'
        verbose_name_plural = u'Учителя'
        db_table = u'catalogs_teachers'
        default_permissions = ()
        permissions = (
            ('add_teacher_entity', 'Добавление информации учителя'),
            ('update_teacher_entity', 'Редактирование информации по учителю'),
            ('delete_teacher_entity', 'Удаление информации по учителю'),
        )


