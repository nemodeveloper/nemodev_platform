# -*- coding: utf-8 -*-
from django.views.generic import DeleteView


class SimpleAddOrUpdateView(object):

    def get_form_mode(self):
        raise NotImplementedError()

    def get_context_data(self, **kwargs):
        context = super(SimpleAddOrUpdateView, self).get_context_data(**kwargs)
        context['form_mode'] = self.get_form_mode()

        return context

    def form_valid(self, form):
        response = super(SimpleAddOrUpdateView, self).form_valid(form)
        return response


class SimpleDeleteView(DeleteView):

    pk_url_kwarg = 'id'

