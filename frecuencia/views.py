# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Frecuencia
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .forms import FrecuenciaSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from home.functions import pagination

# Create your views here.
# Frecuencia
class FrecuenciaCreate(LoginRequiredMixin, CreateView):
    model = Frecuencia
    fields = ['est_id', 'var_id', 'fre_valor', 'fre_fecha_ini', 'fre_fecha_fin']

    def form_valid(self, form):
        return super(FrecuenciaCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FrecuenciaCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context


class FrecuenciaList(LoginRequiredMixin, ListView, FormView):
    # parámetros ListView
    model = Frecuencia
    paginate_by = 10
    # parámetros FormView
    template_name = 'frecuencia/frecuencia_list.html'
    form_class = FrecuenciaSearchForm

    def post(self, request, *args, **kwargs):
        form = FrecuenciaSearchForm(self.request.POST or None)
        page = kwargs.get('page')
        if form.is_valid() and self.request.is_ajax():
            self.object_list = form.filtrar(form)
        else:
            self.object_list = Frecuencia.objects.all()
        context = super(FrecuenciaList, self).get_context_data(**kwargs)
        context.update(pagination(self.object_list, page, 10))
        return render(request, 'frecuencia/frecuencia_table.html', context)

    def get_context_data(self, **kwargs):
        context = super(FrecuenciaList, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        context.update(pagination(self.object_list, page, 10))
        return context


class FrecuenciaDetail(LoginRequiredMixin, DetailView):
    model = Frecuencia


class FrecuenciaUpdate(LoginRequiredMixin, UpdateView):
    model = Frecuencia
    fields = ['est_id', 'var_id', 'fre_fecha_ini', 'fre_fecha_fin']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FrecuenciaUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class FrecuenciaDelete(LoginRequiredMixin, DeleteView):
    model = Frecuencia
    success_url = reverse_lazy('frecuencia:frecuencia_index')

