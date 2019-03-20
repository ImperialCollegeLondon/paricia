# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from importacion.models import Importacion, ImportacionTemp

from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from importacion.functions import (consultar_formatos, validar_fechas,
                                   preformato_matriz, guardar_datos__temp_a_final)
from importacion.forms import ImportacionForm, ImportacionSearchForm
from importacion.lectura import iniciar_lectura
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from home.functions import pagination
import os



class ImportacionList(LoginRequiredMixin, ListView, FormView):
    model = Importacion
    form_class = ImportacionSearchForm
    paginate_by = 10
    queryset = Importacion.objects.filter(imp_tipo ='c')

    def post(self, request, *args, **kwargs):
        form = ImportacionSearchForm(self.request.POST or None)
        page = kwargs.get('page')
        if form.is_valid() and self.request.is_ajax():
            self.object_list = form.filtrar(form, 'c')
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
            self.object_list = form.filtrar(form, 'a')
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


# Vista para cargar el archivo y leer los datos
class ImportacionCreate(LoginRequiredMixin, CreateView):
    model = ImportacionTemp
    fields = ['est_id', 'for_id', 'imp_archivo']
    template_name = 'importacion/importacion_form.html'

    def form_valid(self, form):
        archivo = self.request.FILES['imp_archivo']
        matriz = preformato_matriz(archivo, form.cleaned_data['for_id'])
        form.instance.imp_fecha_ini = matriz.loc[0, 'fecha']
        form.instance.imp_fecha_fin = matriz.loc[matriz.shape[0] - 1, 'fecha']
        form.instance.usuario = self.request.user
        return super(ImportacionCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ImportacionCreate, self).get_context_data(**kwargs)
        context['title'] = "Subir Archivo"
        return context


class ImportacionDelete(LoginRequiredMixin, DeleteView):
    model = Importacion
    success_url = reverse_lazy('importacion:importacion_index')


# Vista para confirmar la importación de datos crudos
class ImportacionConfirm(LoginRequiredMixin, DetailView, FormView):
    model = ImportacionTemp
    template_name = 'importacion/importacion_confirm.html'
    form_class = ImportacionForm
    existe_vacio = False

    def post(self, request, *args, **kwargs):
        form = ImportacionForm(request.POST or None)
        if form.is_valid():
            if request.POST['accion'] == 'confirmar':
                imp_id__temp = kwargs.get('pk')
                imp_id = guardar_datos__temp_a_final(imp_id__temp, form)
                importacion = Importacion.objects.get(imp_id=imp_id)
                clasificaciones = importacion.for_id.clasificacion_set.all()
                variables = []
                for clasificacion in clasificaciones:
                    variables.append(clasificacion.var_id_id)
                return render(request, 'importacion/mensaje.html', {'mensaje': 'Informacion Cargada'})
            elif request.POST['accion'] == 'cancelar':
                return self.render_to_response(self.get_context_data(form=form))
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(ImportacionConfirm, self).get_context_data(**kwargs)
        ## TODO verificar si hay sobreescritura de datos por consulta
        informacion, self.existe_vacio = validar_fechas(self.object)
        context['informacion'] = informacion
        context['existe_vacio'] = self.existe_vacio
        context['nombre_archivo_solo'] = os.path.basename(self.object.imp_archivo.name)
        return context


# lista de formatos por estacion y datalogger
def lista_formatos(request):
    mar_id = request.GET.get('datalogger', None)
    datos = consultar_formatos(mar_id)
    return JsonResponse(datos)

