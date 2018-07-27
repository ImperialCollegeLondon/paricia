# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from importacion.models import Importacion

from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from importacion.functions import (consultar_formatos, guardar_datos,
                                   get_fechas_archivo, validar_fechas)
from importacion.forms import ImportacionForm, ImportacionSearchForm
from importacion.lectura import iniciar_lectura
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from home.functions import pagination


class ImportacionList(LoginRequiredMixin, ListView, FormView):
    model = Importacion
    form_class = ImportacionSearchForm
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        form = ImportacionSearchForm(self.request.POST or None)
        page = kwargs.get('page')
        if form.is_valid() and self.request.is_ajax():
            self.object_list = form.filtrar(form,'c')
        else:
            self.object_list = Importacion.objects.filter(imp_tipo='c')
        context = super(ImportacionList, self).get_context_data(**kwargs)
        context.update(pagination(self.object_list, page, 10))
        return render(request, 'importacion/importacion_table.html', context)

    def get_context_data(self, **kwargs):
        context = super(ImportacionList, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        context.update(pagination(self.object_list, page, 10))
        return context

class ListAutomatico(LoginRequiredMixin, ListView, FormView):
    model = Importacion
    form_class = ImportacionSearchForm
    template_name = 'importacion/automatica_list.html'
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        form = ImportacionSearchForm(self.request.POST or None)
        page = kwargs.get('page')
        if form.is_valid() and self.request.is_ajax():
            self.object_list = form.filtrar(form,'a')
        else:
            self.object_list = Importacion.objects.filter(imp_tipo='a')
        context = super(ListAutomatico, self).get_context_data(**kwargs)
        context.update(pagination(self.object_list, page, 10))
        return render(request, 'importacion/automatica_table.html', context)

    def get_context_data(self, **kwargs):
        context = super(ListAutomatico, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        context.update(pagination(self.object_list, page, 10))
        return context


class ImportacionDetail(LoginRequiredMixin, DetailView, FormView):
    model = Importacion
    template_name = 'importacion/importacion_detail.html'
    form_class = ImportacionForm
    # parametros propios
    existe_vacio = False

    def post(self, request, *args, **kwargs):
        form = ImportacionForm(request.POST or None)
        if form.is_valid():
            imp_id = kwargs.get('pk')
            with transaction.atomic():
                guardar_datos(imp_id, form)
            return render(request, 'importacion/mensaje.html', {'mensaje': 'Informacion Cargada'})
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(ImportacionDetail, self).get_context_data(**kwargs)
        informacion, self.existe_vacio = validar_fechas(self.object)
        context['informacion'] = informacion
        context['existe_vacio'] = self.existe_vacio
        return context


class ImportacionCreate(LoginRequiredMixin, CreateView):
    model = Importacion
    fields = ['est_id', 'for_id', 'imp_archivo']

    def form_valid(self, form):
        archivo = self.request.FILES['imp_archivo']
        form = get_fechas_archivo(archivo, form.instance.for_id, form)
        form.instance.usuario = self.request.user
        return super(ImportacionCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ImportacionCreate, self).get_context_data(**kwargs)
        context['title'] = "Subir Archivo"
        return context


class ImportacionDelete(LoginRequiredMixin, DeleteView):
    model = Importacion
    success_url = reverse_lazy('importacion:importacion_index')


def guardar_archivo(request, imp_id):
    # sobreescribir=request.GET.get('sobreescribir',None)
    # with transaction.atomic():
    # guardar_datos(imp_id)
    return render(request, 'importacion/mensaje.html', {'mensaje': 'Informacion Cargada'})


# lista de formatos por estacion y datalogger
def lista_formatos(request):
    mar_id = request.GET.get('datalogger', None)
    datos = consultar_formatos(mar_id)
    return JsonResponse(datos)


# lectura automática funcion de prueba
def lectura_automatica(request):
    # iniciar_lectura()
    iniciar_lectura()
    datos = {
        'datos': 'Lectura Iniciada'
    }
    return JsonResponse(datos)
