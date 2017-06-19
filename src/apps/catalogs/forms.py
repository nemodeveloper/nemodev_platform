# -*- coding: utf-8 -*-
from django import forms

from src.apps.catalogs.models import ClassRoom, Subject


class ClassRoomForm(forms.ModelForm):

    class Meta:
        model = ClassRoom
        fields = '__all__'


class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = '__all__'