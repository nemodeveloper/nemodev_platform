from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView

from src.apps.catalogs.forms import ClassRoomForm, SubjectForm
from src.apps.catalogs.models import ClassRoom, Subject

from src.base.view.common import SimpleAddOrUpdateView, SimpleDeleteView


# Просмотр списка учебных кабинетов
class ClassRoomListView(ListView):

    model = ClassRoom
    context_object_name = 'classrooms'
    template_name = 'catalogs/classroom/list.html'


class ClassRoomAddOrUpdateBaseView(SimpleAddOrUpdateView):

    model = ClassRoom
    form_class = ClassRoomForm
    template_name = 'catalogs/classroom/edit.html'

    def get_success_url(self):
        return reverse(viewname='classroom_list_view')


class ClassRoomAddView(ClassRoomAddOrUpdateBaseView, CreateView):

    def get_form_mode(self):
        return 'add'


class ClassRoomUpdateView(ClassRoomAddOrUpdateBaseView, UpdateView):

    pk_url_kwarg = 'id'

    def get_form_mode(self):
        return 'edit'


class ClassRoomDeleteView(SimpleDeleteView):
    pass


class SubjectAddOrUpdateBaseView(SimpleAddOrUpdateView):

    model = Subject
    form_class = SubjectForm
    template_name = 'catalogs/subject/edit.html'


class SubjectAddView(SubjectAddOrUpdateBaseView, CreateView):

    def get_form_mode(self):
        return 'add'


class SubjectUpdateView(SubjectAddOrUpdateBaseView, UpdateView):

    def get_form_mode(self):
        return 'edit'


class SubjectDeleteView(SimpleDeleteView):

    def delete(self, request, *args, **kwargs):
        subject = None