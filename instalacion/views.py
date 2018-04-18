# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from instalacion.models import Instalacion
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from instalacion.forms import InstalacionSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from home.functions import pagination


# Variable views
class InstalacionCreate(LoginRequiredMixin, CreateView):
    model = Instalacion
    fields = ['ins_id', 'est_id', 'dat_id', 'ins_fecha_ini', 'ins_fecha_fin', 'ins_en_uso', 'ins_observacion']

    def form_valid(self, form):
        return super(InstalacionCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InstalacionCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context


class InstalacionList(LoginRequiredMixin, ListView, FormView):
    model = Instalacion
    paginate_by = 10
    template_name = 'instalacion/instalacion_list.html'
    form_class = InstalacionSearchForm

    def post(self, request, *args, **kwargs):
        form = InstalacionSearchForm(self.request.POST or None)
        page = kwargs.get('page')

        if form.is_valid():
            self.object_list = form.filtrar(form)
        else:
            self.object_list = Instalacion.objects.all()
        context = super(InstalacionList, self).get_context_data(**kwargs)
        context.update(pagination(self.object_list, page, 10))
        return render(request, 'instalacion/instalacion_table.html', context)

    def get_context_data(self, **kwargs):
        context = super(InstalacionList, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        context.update(pagination(self.object_list, page, 10))
        return context


class InstalacionDetail(LoginRequiredMixin, DetailView):
    model = Instalacion


class InstalacionUpdate(LoginRequiredMixin, UpdateView):
    model = Instalacion
    fields = ['ins_id', 'est_id', 'dat_id', 'ins_fecha_ini', 'ins_fecha_fin', 'ins_en_uso', 'ins_observacion']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InstalacionUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class InstalacionDelete(LoginRequiredMixin, DeleteView):
    model = Instalacion
    success_url = reverse_lazy('instalacion:instalacion_index')
