# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Vacios
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import VaciosSearchForm, DiasVaciosForm
from django.contrib.auth.mixins import LoginRequiredMixin
from home.functions import pagination
from vacios.functions import consultar_dias,dias_sin_datos

# Create your views here.
# Vacios
class VaciosCreate(LoginRequiredMixin, CreateView):
    model = Vacios
    fields = ['est_id', 'var_id', 'vac_fecha_ini', 'vac_hora_ini', 'vac_fecha_fin', 'vac_hora_fin', 'vac_observacion']

    def form_valid(self, form):
        return super(VaciosCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(VaciosCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context


class VaciosList(LoginRequiredMixin, ListView, FormView):
    # parámetros ListView
    model = Vacios
    paginate_by = 10
    # parámetros FormView
    template_name = 'vacios/vacios_list.html'
    form_class = VaciosSearchForm

    def post(self, request, *args, **kwargs):
        form = VaciosSearchForm(self.request.POST or None)
        page = kwargs.get('page')
        if form.is_valid() and self.request.is_ajax():
            self.object_list = form.filtrar(form)
        else:
            self.object_list = Vacios.objects.all()
        context = super(VaciosList, self).get_context_data(**kwargs)
        context.update(pagination(self.object_list, page, 10))
        return render(request, 'vacios/vacios_table.html', context)

    def get_context_data(self, **kwargs):
        context = super(VaciosList, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        context.update(pagination(self.object_list, page, 10))
        return context


class VaciosDetail(LoginRequiredMixin, DetailView):
    model = Vacios


class VaciosUpdate(LoginRequiredMixin, UpdateView):
    model = Vacios
    fields = ['est_id', 'var_id', 'vac_fecha_ini', 'vac_hora_ini', 'vac_fecha_fin', 'vac_hora_fin', 'vac_observacion']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(VaciosUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class VaciosDelete(LoginRequiredMixin, DeleteView):
    model = Vacios
    success_url = reverse_lazy('vacios:vacios_index')


class DiasVacios(LoginRequiredMixin, FormView):
    template_name = 'vacios/consulta_dias.html'
    form_class = DiasVaciosForm

    def post(self, request, *args, **kwargs):
        form = DiasVaciosForm(self.request.POST or None)  # type: DiasVaciosForm
        if form.is_valid():
            datos = consultar_dias(form)
            datos_sin_dias = dias_sin_datos(datos, form)
            return render(request, 'vacios/tabla_dias.html', {'datos': datos, 'datos_sin': datos_sin_dias})
        return render(request, 'home/form_error.html', {'form': form})
