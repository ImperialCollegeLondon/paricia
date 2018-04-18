# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from cruce.models import Cruce
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from cruce.forms import CruceSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from home.functions import pagination


# Cruce views
class CruceCreate(LoginRequiredMixin, CreateView):
    model = Cruce
    fields = ['cru_id', 'est_id', 'var_id']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CruceCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context


class CruceList(LoginRequiredMixin, ListView, FormView):
    model = Cruce
    paginate_by = 10
    template_name = 'cruce/cruce_list.html'
    form_class = CruceSearchForm

    def post(self, request, *args, **kwargs):
        form = CruceSearchForm(self.request.POST or None)
        page = kwargs.get('page')
        if form.is_valid() and self.request.is_ajax():
            self.object_list = form.filtrar(form)
        else:
            self.object_list = Cruce.objects.all()
        context = super(CruceList, self).get_context_data(**kwargs)
        context.update(pagination(self.object_list, page, 10))
        return render(request, 'cruce/cruce_table.html', context)

    def get_context_data(self, **kwargs):
        context = super(CruceList, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        context.update(pagination(self.object_list, page, 10))
        return context


class CruceDetail(LoginRequiredMixin, DetailView):
    model = Cruce


class CruceUpdate(LoginRequiredMixin, UpdateView):
    model = Cruce
    fields = ['cru_id', 'est_id', 'var_id']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CruceUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class CruceDelete(LoginRequiredMixin, DeleteView):
    model = Cruce
    success_url = reverse_lazy('cruce:cruce_index')
