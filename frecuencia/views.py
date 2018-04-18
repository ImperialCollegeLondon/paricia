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
    # parametros propios
    cadena = str("")

    def get(self, request, *args, **kwargs):
        form = FrecuenciaSearchForm(self.request.GET or None)
        self.object_list = Frecuencia.objects.all()
        if form.is_valid():
            self.object_list = form.filtrar(form)
            self.cadena = form.cadena(form)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(FrecuenciaList, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        context.update(pagination(self.object_list, page, 10))
        context["cadena"] = self.cadena
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


def pagination(lista, page, num_reg):
    # lista=model.objects.all()
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
