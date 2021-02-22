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

from sensor.models import Sensor, Marca, Tipo
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from excel_response import ExcelResponse
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from home.functions import *


class SensorList(PermissionRequiredMixin, TemplateView):
    template_name = 'sensor/sensor_list.html'
    permission_required = 'sensor.view_sensor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = ['sen_id', 'sen_codigo', 'tip_id__tip_nombre', 'mar_id__mar_nombre', 'sen_modelo', 'sen_serial', 'sen_estado',]
        modelo = Sensor.objects.values_list(*campos)
        context['sensores'] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class SensorCreate(PermissionRequiredMixin, CreateView):
    model = Sensor
    permission_required = 'sensor.add_sensor'
    fields = [ 'sen_codigo','tip_id', 'mar_id', 'sen_modelo', 'sen_serial', 'sen_estado']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class SensorDetail(PermissionRequiredMixin, DetailView):
    model = Sensor
    permission_required = 'sensor.view_sensor'


class SensorUpdate(PermissionRequiredMixin, UpdateView):
    model = Sensor
    permission_required = 'sensor.change_sensor'
    fields = [ 'sen_codigo','tip_id', 'mar_id', 'sen_modelo', 'sen_serial', 'sen_estado']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class SensorDelete(PermissionRequiredMixin, DeleteView):
    model = Sensor
    permission_required = 'sensor.delete_sensor'
    success_url = reverse_lazy('sensor:sensor_index')



@permission_required('sensor.view_sensor')
def SensorExport(request):
    if request.user.is_authenticated:
        cabecera = [['Código', 'Tipo', 'Marca', 'Modelo', 'Serial'],]
        cuerpo = []
        objetos = Sensor.objects.all()
        for objeto in objetos:
            fila = []
            fila.append(objeto.sen_codigo)
            fila.append(objeto.tip_id.tip_nombre if objeto.tip_id is not None else None)
            fila.append(objeto.mar_id.mar_nombre if objeto.mar_id is not None else None)
            fila.append(objeto.sen_modelo)
            fila.append(objeto.sen_serial)
            cuerpo.append(fila)
        response = ExcelResponse(cabecera + cuerpo, 'Sensores_iMHEA')
        return response


@permission_required('sensor.view_sensor')
def ListaSensores(request):
    sensores = Sensor.objects.all()
    lista = []
    for row in sensores:
        linea = row.sen_codigo + " -- " + \
                ("" if row.sen_modelo is None else row.sen_modelo + " - ")
        lista.append(linea)
    return JsonResponse({'lista': lista})


# #  MARCA


class MarcaList(PermissionRequiredMixin, TemplateView):
    template_name = 'sensor/marca_list.html'
    permission_required = 'sensor.view_marca'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = ['mar_id', 'mar_nombre', ]
        modelo = Marca.objects.values_list(*campos)
        context['marcas'] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class MarcaCreate(PermissionRequiredMixin, CreateView):
    model = Marca
    permission_required = 'sensor.add_marca'
    fields = ['mar_nombre']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class MarcaDetail(PermissionRequiredMixin, DetailView):
    model = Marca
    permission_required = 'sensor.view_marca'


class MarcaUpdate(PermissionRequiredMixin, UpdateView):
    model = Marca
    permission_required = 'sensor.change_marca'
    fields = ['mar_nombre']

    def get_context_data(self, **kwargs):
        context = super(MarcaUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class MarcaDelete(PermissionRequiredMixin, DeleteView):
    model = Marca
    permission_required = 'sensor.delete_marca'
    success_url = reverse_lazy('sensor:marca_index')



# Tipo
class TipoList(PermissionRequiredMixin, TemplateView):
    template_name = 'sensor/tipo_list.html'
    permission_required = 'sensor.view_tipo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = ['tip_id', 'tip_nombre', ]
        modelo = Tipo.objects.values_list(*campos)
        context['tipos'] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class TipoCreate(PermissionRequiredMixin, CreateView):
    model = Tipo
    permission_required = 'sensor.add_tipo'
    fields = ['tip_nombre']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class TipoDetail(PermissionRequiredMixin, DetailView):
    model = Tipo
    permission_required = 'sensor.view_tipo'


class TipoUpdate(PermissionRequiredMixin, UpdateView):
    model = Tipo
    permission_required = 'sensor.change_tipo'
    fields = ['tip_nombre']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class TipoDelete(PermissionRequiredMixin, DeleteView):
    model = Tipo
    permission_required = 'sensor.delete_tipo'
    success_url = reverse_lazy('sensor:tipo_index')