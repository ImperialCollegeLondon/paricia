# -*- coding: utf-8 -*-

################################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos (iMHEA)
# basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#         Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS), Ecuador.
#         Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones creadoras,
#              ya sea en uso total o parcial del código.

from __future__ import unicode_literals

from datalogger.models import Datalogger, Marca
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from home.functions import *
from .functions import *


class DataloggerList(PermissionRequiredMixin, TemplateView):
    template_name = 'datalogger/datalogger_list.html'
    permission_required = 'datalogger.view_datalogger'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = ['dat_id', 'dat_codigo', 'dat_modelo', 'dat_serial', 'dat_estado', 'mar_id__mar_nombre']
        modelo = Datalogger.objects.values_list(*campos)
        context['dataloggers'] = modelo_a_tabla_html(modelo, col_extra=True)
        context['marcas'] = Marca.objects.all()
        return context


class DataloggerCreate(PermissionRequiredMixin, CreateView):
    model = Datalogger
    permission_required = 'datalogger.add_datalogger'
    fields = ['dat_codigo', 'mar_id', 'dat_modelo', 'dat_serial', 'dat_estado']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class DataloggerDetail(DetailView):
    model = Datalogger
    permission_required = 'datalogger.view_datalogger'


class DataloggerUpdate(PermissionRequiredMixin, UpdateView):
    model = Datalogger
    permission_required = 'datalogger.change_datalogger'
    fields = ['dat_codigo', 'mar_id', 'dat_modelo', 'dat_serial', 'dat_estado']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class DataloggerDelete(PermissionRequiredMixin, DeleteView):
    model = Datalogger
    permission_required = 'datalogger.delete_datalogger'
    success_url = reverse_lazy('datalogger:datalogger_index')


@permission_required('datalogger.view_datalogger')
def DataloggerExport(request):
    response = excel_datalogger()
    return response


# @permission_required('datalogger.view_datalogger')
# def ListaDataloggers(request):
#     dataloggers = Datalogger.objects.all()
#     lista = []
#     for row in dataloggers:
#         linea = row.dat_codigo + " -- " + \
#                 ("" if row.dat_modelo is None else row.dat_modelo + " - ") + \
#                 ("" if row.dat_serial is None else row.dat_serial)
#         lista.append(linea)
#     return JsonResponse({'lista': lista})


#################################################################################

class MarcaList(PermissionRequiredMixin, TemplateView):
    template_name = 'datalogger/marca_list.html'
    permission_required = 'datalogger.view_marca'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = ['mar_id', 'mar_nombre', ]
        modelo = Marca.objects.values_list(*campos)
        context['marcas'] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class MarcaCreate(PermissionRequiredMixin, CreateView):
    model = Marca
    permission_required = 'datalogger.add_marca'
    fields = ['mar_nombre']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class MarcaDetail(DetailView):
    model = Marca
    permission_required = 'datalogger.view_marca'


class MarcaUpdate(PermissionRequiredMixin, UpdateView):
    model = Marca
    permission_required = 'datalogger.change_marca'
    fields = ['mar_nombre']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class MarcaDelete(PermissionRequiredMixin, DeleteView):
    model = Marca
    permission_required = 'datalogger.delete_marca'
    success_url = reverse_lazy('datalogger:marca_index')


