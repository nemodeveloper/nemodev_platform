from django.db import models

# Create your models here.
from src.apps.quotes.manager import QuoteManager, AuthorManager, CategoryManager


class Author(models.Model):

    full_name = models.CharField(u'ФИО', max_length=40, db_index=True)

    objects = models.Manager()
    author_manager = AuthorManager()

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = u'Автор'
        verbose_name_plural = u'Авторы'
        db_table = u'quotes_author'
        default_permissions = ()
        permissions = (
            ('add_author', 'Добавление автора'),
            ('change_author', 'Обновление информации автора'),
            ('delete_author', 'Удаление автора'),
        )


class Category(models.Model):

    name = models.CharField(u'Название', max_length=20, unique=True, db_index=True)

    objects = models.Manager()
    category_manager = CategoryManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'
        db_table = u'quotes_category'
        default_permissions = ()
        permissions = (
            ('add_category', 'Добавление категории'),
            ('change_category', 'Обновление информации категории'),
            ('delete_category', 'Удаление категории'),
        )


class Quote(models.Model):

    category = models.ForeignKey(to=Category, verbose_name=u'Категория', related_name=u'quotes', related_query_name=u'quote', on_delete=models.PROTECT)
    text = models.TextField(u'Цитата')
    author = models.ForeignKey(to=Author, verbose_name=u'Автор', null=True, related_name=u'quotes', related_query_name=u'quote', on_delete=models.SET_NULL)
    source = models.CharField(u'Ресурс', max_length=50, blank=True, null=True)
    year = models.CharField(u'Год', max_length=20, blank=True, null=True)

    objects = models.Manager()
    quote_manager = QuoteManager()

    def build_quote(self):
        quote = self.text
        if self.author:
            quote += '\n%s' % self.author.full_name
        if self.source:
            quote += '\n%s' % self.source
        if self.year:
            quote += '\n%s' % self.year
        return quote

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = u'Цитата'
        verbose_name_plural = u'Цитаты'
        db_table = u'quotes_quote'
        default_permissions = ()
        permissions = (
            ('add_quote', 'Добавление цитаты'),
            ('change_quote', 'Обновление информации цитаты'),
            ('delete_quote', 'Удаление цитаты'),
        )
