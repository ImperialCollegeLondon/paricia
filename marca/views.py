# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from marca.models import Marca
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin


# Marca de Datalogger y Sensores
class MarcaCreate(LoginRequiredMixin, CreateView):
    model = Marca
    fields = ['mar_nombre']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MarcaCreate, self).get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class MarcaList(LoginRequiredMixin, ListView):
    # parámetros ListView
    model = Marca
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(MarcaList, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        context.update(pagination(self.object_list, page, 10))
        return context


class MarcaDetail(LoginRequiredMixin, DetailView):
    model = Marca


class MarcaUpdate(LoginRequiredMixin, UpdateView):
    model = Marca
    fields = ['mar_nombre']

    def get_context_data(self, **kwargs):
        context = super(MarcaUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class MarcaDelete(LoginRequiredMixin, DeleteView):
    model = Marca
    success_url = reverse_lazy('marca:marca_index')


def pagination(lista, page, num_reg):

    paginator = Paginator(lista, num_reg)
    if page is None:
        page = 1
    else:
        page = int(page)
    if page == 1:
        start = 1
        last = start + 1
    elif page == paginator.num_pages:
        last = paginator.num_pages
        start = last - 1
    else:
        start = page - 1
        last = page + 1
    context = {
        'first': '1',
        'last': paginator.num_pages,
        'range': range(start, last + 1),
    }
    return context
