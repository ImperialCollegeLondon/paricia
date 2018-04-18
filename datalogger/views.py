# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from datalogger.models import Datalogger
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from datalogger.forms import DataloggerSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from home.functions import pagination


# Datalogger views
class DataloggerCreate(LoginRequiredMixin, CreateView):
    model = Datalogger
    fields = ['est_id', 'dat_codigo', 'mar_id', 'dat_modelo', 'dat_serial']

    def form_valid(self, form):
        return super(DataloggerCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DataloggerCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context


class DataloggerList(LoginRequiredMixin, ListView, FormView):
    # parámetros ListView
    model = Datalogger
    paginate_by = 10
    # parámetros FormView
    template_name = 'datalogger/datalogger_list.html'
    form_class = DataloggerSearchForm

    def post(self, request, *args, **kwargs):
        form = DataloggerSearchForm(self.request.POST or None)
        page = kwargs.get('page')
        if form.is_valid() and self.request.is_ajax():
            self.object_list = form.filtrar(form)
        else:
            self.object_list = Datalogger.objects.all()
        context = super(DataloggerList, self).get_context_data(**kwargs)
        context.update(pagination(self.object_list, page, 10))
        return render(request, 'datalogger/datalogger_table.html', context)

    def get_context_data(self, **kwargs):
        context = super(DataloggerList, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        context.update(pagination(self.object_list, page, 10))
        return context


class DataloggerDetail(LoginRequiredMixin, DetailView):
    model = Datalogger


class DataloggerUpdate(LoginRequiredMixin, UpdateView):
    model = Datalogger
    fields = ['est_id', 'dat_codigo', 'mar_id', 'dat_modelo', 'dat_serial']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DataloggerUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class DataloggerDelete(LoginRequiredMixin, DeleteView):
    model = Datalogger
    success_url = reverse_lazy('datalogger:datalogger_index')
