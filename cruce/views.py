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

from cruce.models import Cruce
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Value
from django.db.models.functions import Concat
from home.functions import *

class CruceCreate(PermissionRequiredMixin, CreateView):
    model = Cruce
    fields = ['cru_id', 'est_id', 'var_id']
    permission_required = 'cruce.add_cruce'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class CruceList(PermissionRequiredMixin, TemplateView):
    template_name = 'cruce/cruce_list.html'
    permission_required = 'cruce.view_cruce'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = ['cru_id', 'est_id__est_codigo', 'var_id__var_nombre']
        cruce = Cruce.objects.all().values_list(*campos)
        context['cruce'] = modelo_a_tabla_html(cruce, col_extra=True)
        return context


class CruceDetail(PermissionRequiredMixin, DetailView):
    model = Cruce
    permission_required = 'cruce.view_cruce'


class CruceUpdate(PermissionRequiredMixin, UpdateView):
    model = Cruce
    fields = ['cru_id', 'est_id', 'var_id']
    permission_required = 'cruce.change_cruce'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class CruceDelete(PermissionRequiredMixin, DeleteView):
    model = Cruce
    success_url = reverse_lazy('cruce:cruce_index')
    permission_required = 'cruce.delete_cruce'
