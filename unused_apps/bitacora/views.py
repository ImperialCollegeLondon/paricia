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
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from bitacora.models import Bitacora
from home.functions import *


class BitacoraCreate(PermissionRequiredMixin, CreateView):
    model = Bitacora
    fields = ["est_id", "var_id", "bit_fecha_ini", "bit_fecha_fin", "bit_observacion"]
    permission_required = "bitacora.add_bitacora"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear"
        return context


class BitacoraList(PermissionRequiredMixin, TemplateView):
    template_name = "bitacora/bitacora_list.html"
    permission_required = "bitacora.view_bitacora"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = [
            "bit_id",
            "est_id__est_codigo",
            "var_id__var_nombre",
            "bit_fecha_ini",
            "bit_fecha_fin",
            "bit_observacion",
        ]
        bitacora = Bitacora.objects.all().values_list(*campos)
        context["bitacora"] = modelo_a_tabla_html(bitacora, col_extra=True)
        return context


class BitacoraDetail(PermissionRequiredMixin, DetailView):
    model = Bitacora
    permission_required = "bitacora.view_bitacora"


class BitacoraUpdate(PermissionRequiredMixin, UpdateView):
    model = Bitacora
    permission_required = "bitacora.change_bitacora"
    fields = [
        "bit_id",
        "est_id",
        "var_id",
        "bit_fecha_ini",
        "bit_fecha_fin",
        "bit_observacion",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modificar"
        return context


class BitacoraDelete(PermissionRequiredMixin, DeleteView):
    model = Bitacora
    permission_required = "bitacora.delete_bitacora"
    success_url = reverse_lazy("bitacora:bitacora_index")
