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

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Value
from django.db.models.functions import Concat
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from home.functions import *

from .forms import *
from .models import Frecuencia


class FrecuenciaCreate(PermissionRequiredMixin, CreateView):
    model = Frecuencia
    permission_required = "frecuencia.add_frecuencia"
    form_class = CrearFrecuenciaForm
    success_url = reverse_lazy("frecuencia:frecuencia_index")

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear"
        return context


class FrecuenciaList(TemplateView, PermissionRequiredMixin):
    template_name = "frecuencia/frecuencia_list.html"
    permission_required = "frecuencia.view_frecuencia"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = [
            "fre_id",
            "est_id__est_codigo",
            "var_id__var_nombre",
            "fre_valor",
            "fre_fecha_ini",
            "fre_fecha_fin",
        ]
        modelo = Frecuencia.objects.all().values_list(*campos)
        context["frecuencia"] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class FrecuenciaUpdate(PermissionRequiredMixin, UpdateView):
    model = Frecuencia
    permission_required = "frecuencia.change_frecuencia"
    form_class = CrearFrecuenciaForm
    success_url = reverse_lazy("frecuencia:frecuencia_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modificar"
        return context


class FrecuenciaDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "frecuencia.delete_frecuencia"
    model = Frecuencia
    success_url = reverse_lazy("frecuencia:frecuencia_index")
