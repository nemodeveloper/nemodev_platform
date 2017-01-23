from tastypie.resources import ModelResource

from src.apps.ext_user.models import ExtUser


class ExtUserResource(ModelResource):

    list_allowed_methods = ['get']
    detail_allowed_methods = ['get']

    class Meta:
        queryset = ExtUser.objects.all()
        resource_name = 'user'
