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
from .models import Variable, Unidad, Control
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from excel_response import ExcelResponse
from django.db.models import Value
from django.db.models.functions import Concat
from home.functions import *
from django.http import JsonResponse

class VariableCreate(PermissionRequiredMixin, CreateView):
    model = Variable
    permission_required = 'variable.__super__add_variable'
    fields = ['var_codigo', 'var_nombre', 'uni_id', 'var_maximo', 'var_minimo', 'var_sos', 'var_err', 'var_min',
              'var_estado', 'es_acumulada', 'reporte_automatico', 'umbral_completo']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class VariableList(PermissionRequiredMixin, TemplateView):
    template_name = 'variable/variable_list.html'
    permission_required = 'variable.view_variable'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = ['var_id', 'var_codigo', 'var_nombre', 'uni_id__uni_sigla', 'var_maximo', 'var_minimo', 'var_sos',
                  'var_err', 'var_min', 'var_estado', 'es_acumulada', 'reporte_automatico', 'umbral_completo']
        modelo = Variable.objects.values_list(*campos)
        context['variables'] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class VariableDetail(PermissionRequiredMixin,DetailView):
    model = Variable
    permission_required = 'variable.view_variable'


class VariableUpdate(PermissionRequiredMixin, UpdateView):
    model = Variable
    permission_required = 'variable.change_variable'
    fields = ['var_codigo', 'var_nombre', 'uni_id', 'var_maximo', 'var_minimo', 'var_sos', 'var_err', 'var_min',
              'var_estado', 'es_acumulada', 'reporte_automatico', 'umbral_completo']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class VariableDelete(PermissionRequiredMixin, DeleteView):
    model = Variable
    permission_required = 'variable.__super__delete_variable'
    success_url = reverse_lazy('variable:variable_index')


@permission_required('variable.view_variable')
def VariableExport(request):
    cabecera = [['Código', 'Nombre', 'Unidad'],]
    cuerpo = []
    objetos = Variable.objects.all()
    for objeto in objetos:
        fila = []
        fila.append(objeto.var_codigo)
        fila.append(objeto.var_nombre)
        try:
            fila.append('\' '+objeto.uni_id.uni_sigla)
        except:
            fila.append(None)
        cuerpo.append(fila)
    response = ExcelResponse(cabecera + cuerpo, 'Variables_iMHEA')
    return response

##################################################################
# Unidad
class UnidadCreate(PermissionRequiredMixin, CreateView):
    model = Unidad
    permission_required = 'variable.add_unidad'
    fields = ['uni_nombre', 'uni_sigla']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class UnidadList(PermissionRequiredMixin, TemplateView):
    template_name = 'variable/unidad_list.html'
    permission_required = 'variable.view_unidad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = ['uni_id', 'uni_nombre', 'uni_sigla']
        modelo = Unidad.objects.values_list(*campos)
        context['unidades'] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class UnidadDetail(PermissionRequiredMixin, DetailView):
    model = Unidad
    permission_required = 'variable.view_unidad'


class UnidadUpdate(PermissionRequiredMixin, UpdateView):
    model = Unidad
    permission_required = 'variable.change_unidad'
    fields = ['uni_nombre', 'uni_sigla']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class UnidadDelete(PermissionRequiredMixin, DeleteView):
    model = Unidad
    permission_required = 'variable.delete_unidad'
    success_url = reverse_lazy('variable:unidad_index')


####################################################################
# Model Control
class ControlCreate(PermissionRequiredMixin, CreateView):
    model = Control
    permission_required = 'variable.add_control'
    fields = ['var_id', 'sen_id', 'est_id', 'con_fecha_ini', 'con_fecha_fin', 'con_estado']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class ControlList(PermissionRequiredMixin, TemplateView):
    template_name = 'variable/control_list.html'
    permission_required = 'variable.view_control'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _modelo = Control.objects.annotate(
            est_codigo_nombre=Concat('est_id__est_codigo', Value(' - '), 'est_id__est_nombre')
        )
        campos = ['con_id', 'var_id__var_nombre', 'sen_id__sen_codigo', 'est_codigo_nombre', 'con_fecha_ini', 'con_fecha_fin', 'con_estado' ]
        modelo = _modelo.values_list(*campos)
        context['control'] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class ControlDetail(PermissionRequiredMixin, DetailView):
    model = Control
    permission_required = 'variable.view_control'


class ControlUpdate(PermissionRequiredMixin, UpdateView):
    model = Control
    permission_required = 'variable.change_control'
    fields = ['var_id', 'sen_id', 'est_id', 'con_fecha_ini', 'con_fecha_fin', 'con_estado']

    def get_context_data(self, **kwargs):
        context = super(ControlUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class ControlDelete(PermissionRequiredMixin, DeleteView):
    model = Control
    permission_required = 'variable.delete_control'
    success_url = reverse_lazy('variable:control_index')



def get_limites(request):
    print(request.POST.get('var_id'))
    id = int(request.POST.get('var_id'))
    variable = Variable.objects.get(var_id=id)
    data = {
        'var_maximo': variable.var_maximo,
        'var_minimo': variable.var_minimo
    }
    return JsonResponse(data)