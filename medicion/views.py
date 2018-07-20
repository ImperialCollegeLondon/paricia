# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from medicion.models import Medicion
from formato.models import Clasificacion
from importacion.models import Importacion
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from medicion.forms import MedicionSearchForm, FilterDeleteForm, MedicionConsultaForm
from medicion.functions import (filtrar, datos_instantaneos, eliminar,
                                consultar_objeto, modificar_medicion, eliminar_medicion,
                                guardar_log, grafico)
from django.db import connection
from django.contrib.auth.mixins import LoginRequiredMixin


# Medicion views
class MedicionCreate(LoginRequiredMixin, CreateView):
    model = Medicion
    fields = ['var_id', 'est_id', 'med_fecha', 'med_valor', 'med_maximo',
              'med_minimo']

    def form_valid(self, form):
        return super(MedicionCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MedicionCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context


# filtro para la validación de Datos Crudos
class MedicionFilter(LoginRequiredMixin, FormView):
    template_name = 'medicion/medicion_filter.html'
    form_class = MedicionSearchForm
    success_url = '/medicion/filter/'
    lista = []
    variable = ""

    def post(self, request, *args, **kwargs):
        form = MedicionSearchForm(self.request.POST or None)
        if form.is_valid() and self.request.is_ajax():
            self.lista = filtrar(form)
            self.variable = form.cleaned_data['variable']
            return render(request, 'medicion/medicion_list.html',
                          {'lista': self.lista, 'variable': self.variable})
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(MedicionFilter, self).get_context_data(**kwargs)
        context['lista'] = self.lista
        context['variable'] = self.variable
        return context


# Lista de datos crudos
class MedicionList(LoginRequiredMixin, FormView):
    template_name = 'medicion/medicion_list.html'
    form_class = MedicionSearchForm
    success_url = '/medicion/'
    lista = []
    variable = ""

    def post(self, request, *args, **kwargs):
        form = MedicionSearchForm(self.request.POST or None)
        if form.is_valid():
            self.lista = filtrar(form)
            self.variable = form.cleaned_data['variable']
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(MedicionList, self).get_context_data(**kwargs)
        context['lista'] = self.lista
        context['variable'] = self.variable
        return context


# Clase para filtrar datos para la vista delete
class ListDelete(LoginRequiredMixin, FormView, ListView):
    template_name = 'medicion/list_delete.html'
    form_class = FilterDeleteForm
    success_url = '/medicion/listdelete/'
    model = Medicion
    variable = ""

    def post(self, request, *args, **kwargs):
        form = FilterDeleteForm(self.request.POST or None)
        if form.is_valid():
            self.lista = consultar(form)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(ListDelete, self).get_context_data(**kwargs)
        context['lista'] = self.lista
        return context


# filtro para eliminar los datos
class FilterDelete(LoginRequiredMixin, FormView):
    template_name = 'medicion/filter_delete.html'
    form_class = FilterDeleteForm
    success_url = '/medicion/filterdelete/'
    # mensaje de confirmación
    mensaje = ""

    def post(self, request, *args, **kwargs):
        form = FilterDeleteForm(self.request.POST or None)
        if form.is_valid():
            eliminar(form)
            self.mensaje = "Datos Eliminados"
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(FilterDelete, self).get_context_data(**kwargs)
        context['mensaje'] = self.mensaje
        return context


class MedicionUpdate(LoginRequiredMixin, UpdateView):
    model = Medicion
    fields = ['med_valor', 'med_maximo', 'med_minimo']
    url = ""

    def get(self, request, *args, **kwargs):
        med_id = kwargs.get('pk')
        med_fecha = kwargs.get('fecha')
        var_id = kwargs.get('var_id')
        self.object = consultar_objeto(kwargs)
        self.url = "/medicion/" + med_id + "/" + med_fecha + "/" + var_id + "/"
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        modificar_medicion(kwargs, request.POST)
        self.object = consultar_objeto(kwargs)
        guardar_log(accion="Modificar", medicion=self.object, user=request.user)
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MedicionUpdate, self).get_context_data(**kwargs)
        context['url'] = self.url
        return context


class MedicionDelete(LoginRequiredMixin, UpdateView):
    model = Medicion
    fields = ['est_id', 'var_id', 'med_fecha', 'med_valor', 'med_valor', 'med_maximo', 'med_minimo']
    url = ""
    template_name = 'medicion/medicion_delete.html'

    def get(self, request, *args, **kwargs):
        med_id = kwargs.get('pk')
        med_fecha = kwargs.get('fecha')
        var_id = kwargs.get('var_id')
        self.object = consultar_objeto(kwargs)
        self.url = "/medicion/delete/" + med_id + "/" + med_fecha + "/" + var_id + "/"
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        eliminar_medicion(kwargs, request.POST)
        self.object = consultar_objeto(kwargs)
        guardar_log(accion="Eliminar", medicion=self.object, user=request.user)
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MedicionDelete, self).get_context_data(**kwargs)
        context['url'] = self.url
        return context


'''class MedicionImportacion(LoginRequiredMixin, FormView):
    model = Medicion
    template_name = 'medicion/medicion_importacion.html'
    form_class = MedicionSearchForm

    def get(self, request, *args, **kwargs):
        imp_id = kwargs.get('imp_id')
        importacion = Importacion.objects.get(imp_id=imp_id)
        clasificacion = Clasificacion.objects.filter(for_id=importacion.for_id)
        context = []
        for fila in clasificacion:
            data = {
                'estacion': importacion.est_id.est_id,
                'variable': fila.var_id.var_id,
                'inicio': importacion.imp_fecha_ini.strftime('%d/%m/%Y'),
                'fin': importacion.imp_fecha_fin.strftime('%d/%m/%Y')
            }
            form = MedicionSearchForm(data)
            if form.is_valid():
                # context[str(fila.var_id.var_codigo)]=consultar(form)
                consulta = consultar(form)
                obj_informacion = Informacion()
                obj_informacion.nombre = fila.var_id.var_nombre
                obj_informacion.lista = consulta
                obj_informacion.grafico = grafico(consulta, fila.var_id, importacion.est_id)
                context.append(obj_informacion)
            else:
                context = []
        return self.render_to_response(self.get_context_data(informacion=context, form=form))

    def get_context_data(self, **kwargs):
        context = super(MedicionImportacion, self).get_context_data(**kwargs)
        return context'''


class MedicionConsulta(LoginRequiredMixin,FormView):
    template_name = 'medicion/consulta.html'
    form_class = MedicionConsultaForm
    success_url = '/medicion/consulta'
    grafico = []

    def post(self, request, *args, **kwargs):
        form = MedicionConsultaForm(self.request.POST or None)
        if form.is_valid() and self.request.is_ajax():
            valores, maximos_abs, minimos_abs, tiempo = datos_instantaneos(form)
            self.grafico = grafico(form, valores, maximos_abs, minimos_abs, tiempo)
            return render(request, 'reportes/consultas/grafico.html',
                          {'grafico': self.grafico})
        # elif form.is_valid():
            # return self.export_excel(self.frecuencia, form)
        return render(request, 'home/form_error.html', {'form': form})
