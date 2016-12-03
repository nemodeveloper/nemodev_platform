from tastypie.resources import ModelResource

from src.apps.ext_user.models import ExtUser


class ExtUserResource(ModelResource):

    class Meta:
        queryset = ExtUser.objects.all()
        resource_name = 'user'
