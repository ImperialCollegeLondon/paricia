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
from medicion.models import CurvaDescarga
from .forms import CurvaDescargaForm
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from home.functions import *
from django.contrib.auth.decorators import permission_required
from variable.models import Variable
from django.db.models import Prefetch
from cruce.models import Cruce
from django.http import JsonResponse
from django.db.models import Value
from django.db.models.functions import Concat


class CurvaDescargaList(PermissionRequiredMixin, TemplateView):
    template_name = 'medicion/curvadescarga_list.html'
    permission_required = 'medicion.view_curvadescarga'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _modelo = CurvaDescarga.objects.annotate(
            est_codigo_nombre=Concat('estacion__est_codigo', Value(' - '), 'estacion__est_nombre')
        )
        campos = ['id', 'est_codigo_nombre', 'fecha', 'funcion']
        modelo = _modelo.values_list(*campos)
        context['curvadescarga'] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class CurvaDescargaCreate(PermissionRequiredMixin, CreateView):
    template_name = 'medicion/curvadescarga_form.html'
    permission_required = 'medicion.add_curvadescarga'
    form_class = CurvaDescargaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class CurvaDescargaDetail(PermissionRequiredMixin, DetailView):
    model = CurvaDescarga
    permission_required = 'medicion.view_curvadescarga'


class CurvaDescargaUpdate(PermissionRequiredMixin, UpdateView):
    model = CurvaDescarga
    permission_required = 'medicion.change_curvadescarga'
    fields = ['estacion', 'fecha', 'funcion']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class CurvaDescargaDelete(PermissionRequiredMixin, DeleteView):
    model = CurvaDescarga
    permission_required = 'medicion.delete_curvadescarga'
    success_url = reverse_lazy('medicion:curvadescarga_index')


@permission_required('medicion.validar')
def variables(request):
    try:
        estacion_id = int(request.GET.get('estacion_id', None))
    except ValueError:
        estacion_id = None
    if estacion_id is not None:
        variables = Cruce.objects.prefetch_related(
            Prefetch('var_id', queryset=Variable.objects.all())
        ).filter(est_id=estacion_id)
    else:
        variables = Variable.objects.all()
    lista = {}
    for row in variables:
        lista[row.var_id.var_id] = row.var_id.var_nombre
    return JsonResponse(lista)
