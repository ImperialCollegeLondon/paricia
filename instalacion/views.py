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
from instalacion.models import Instalacion
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Value
from django.db.models.functions import Concat
from home.functions import *


class InstalacionCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'instalacion.add_instalacion'
    model = Instalacion
    fields = ['ins_id', 'est_id', 'dat_id', 'ins_fecha_ini', 'ins_fecha_fin', 'ins_en_uso', 'ins_observacion']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class InstalacionList(PermissionRequiredMixin, TemplateView):
    template_name = 'instalacion/instalacion_list.html'
    permission_required = 'instalacion.view_instalacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _modelo = Instalacion.objects.annotate(
            est_codigo_nombre=Concat('est_id__est_codigo', Value(' - '), 'est_id__est_nombre')
        )
        campos = ['ins_id', 'est_codigo_nombre', 'dat_id__dat_codigo', 'ins_fecha_ini', 'ins_fecha_fin', 'ins_en_uso', 'ins_observacion']
        modelo = _modelo.values_list(*campos)
        context['instalacion'] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class InstalacionDetail(PermissionRequiredMixin, DetailView):
    model = Instalacion
    permission_required = 'instalacion.view_instalacion'


class InstalacionUpdate(PermissionRequiredMixin, UpdateView):
    model = Instalacion
    fields = ['ins_id', 'est_id', 'dat_id', 'ins_fecha_ini', 'ins_fecha_fin', 'ins_en_uso', 'ins_observacion']
    permission_required = 'instalacion.change_instalacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class InstalacionDelete(PermissionRequiredMixin, DeleteView):
    model = Instalacion
    success_url = reverse_lazy('instalacion:instalacion_index')
    permission_required = 'instalacion.delete_instalacion'
