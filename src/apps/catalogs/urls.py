# -*- coding: utf-8 -*-
from django.conf.urls import url

from src.apps.catalogs.views import ClassRoomAddView, ClassRoomUpdateView, ClassRoomDeleteView, ClassRoomListView

urlpatterns = (
    url(r'^classroom/list/$', view=ClassRoomListView.as_view(), name='classroom_list_view'),
    url(r'^classroom/add/$', view=ClassRoomAddView.as_view(), name='classroom_add_view'),
    url(r'^classroom/update/(?P<id>\d+)$', view=ClassRoomUpdateView.as_view(), name='classroom_update_view'),
    url(r'^classroom/delete/(?P<id>\d+)$', view=ClassRoomDeleteView.as_view(), name='classroom_delete_view'),

    # url(r'^subject/add/$', view=, name='subject_add'),
    # url(r'^subject/edit/(?P<id>\d+)$', view=, name='subject_update'),
    # url(r'^subject/delete/(?P<id>\d+)$', view=, name='subject_delete'),

    # url(r'^schoolclass/add/$', view=, name='schoolclass_add'),
    # url(r'^schoolclass/edit/(?P<id>\d+)$', view=, name='schoolclass_update'),
    # url(r'^schoolclass/delete/(?P<id>\d+)$', view=, name='schoolclass_delete'),
    #
    # url(r'^teacher/add/$', view=, name='teacher_add'),
    # url(r'^teacher/edit/(?P<id>\d+)$', view=, name='teacher_update'),
    # url(r'^teacher/delete/(?P<id>\d+)$', view=, name='teacher_delete'),
    #
    # url(r'^lessontime/add/$', view=, name='lessontimeadd'),
    # url(r'^lessontime/edit/(?P<id>\d+)$', view=, name='lessontime_update'),
    # url(r'^lessontime/delete/(?P<id>\d+)$', view=, name='lessontime_delete'),
)

