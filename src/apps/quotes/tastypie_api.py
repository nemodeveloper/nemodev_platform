# -*- coding: utf-8 -*-
from tastypie import fields
from tastypie.constants import ALL
from tastypie.resources import ModelResource

from src.apps.quotes.models import Quote, Category, Author


class AuthorResource(ModelResource):

    list_allowed_methods = ['get']
    detail_allowed_methods = ['get']

    class Meta:
        queryset = Author.objects.all()
        resource_name = 'author'


class CategoryResource(ModelResource):

    list_allowed_methods = ['get']
    detail_allowed_methods = ['get']

    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'
        limit = 0


class QuoteResource(ModelResource):

    author = fields.ForeignKey(AuthorResource, 'author', null=True, full=True, full_list=False, full_detail=True)
    category = fields.ForeignKey(CategoryResource, 'category', full=True, full_list=False, full_detail=True)

    list_allowed_methods = ['get']
    detail_allowed_methods = ['get']

    class Meta:
        queryset = Quote.objects.select_related().all()
        resource_name = 'quote'
        filtering = {
            'category': ALL
        }
        limit = 150
